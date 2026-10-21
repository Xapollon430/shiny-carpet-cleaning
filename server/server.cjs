const http = require('node:http');
const fs = require('node:fs/promises');
const path = require('node:path');
const crypto = require('node:crypto');
const redirects = new Map(require('node:fs').readFileSync(path.resolve(__dirname,'../dist/_redirects'),'utf8').split('\n').filter(line=>line.trim() && !line.trim().startsWith('#')).map(line=>{ const [from,to,status]=line.trim().split(/\s+/); return [from,{to,status:Number(status)}]; }));
const { renderEmail } = require('../emails/render.cjs');
const root = path.resolve(__dirname, '../dist');
const dataDir = process.env.DATA_DIR || '/var/lib/shiny';
const siteUrl = process.env.SITE_URL || 'http://localhost:8000';
const required = {
  'quote-request': ['name','email','phone','zip','service'],
  'contact-message': ['name','email','message'],
  'career-application': ['name','email','phone','position','location','availability','message'],
};
const attempts = new Map();
const mime = {'.html':'text/html; charset=utf-8','.css':'text/css','.js':'application/javascript','.svg':'image/svg+xml','.jpg':'image/jpeg','.jpeg':'image/jpeg','.png':'image/png','.webp':'image/webp','.woff2':'font/woff2','.json':'application/json','.xml':'application/xml','.txt':'text/plain','.ico':'image/x-icon'};
function reply(res, code, body) { res.writeHead(code, {'Content-Type':'application/json','Cache-Control':'no-store'}); res.end(JSON.stringify(body)); }
async function submit(req, res) {
  if (req.headers.origin && req.headers.origin !== new URL(siteUrl).origin) return reply(res,403,{error:'Invalid origin'});
  const now=Date.now();
  for (const [key,value] of attempts) if(now-value.start>600000) attempts.delete(key);
  const ip=String(req.headers['x-forwarded-for'] || req.socket.remoteAddress).split(',')[0].trim();
  const attempt=attempts.get(ip) || {start:now,count:0}; attempts.set(ip,attempt);
  if (++attempt.count > 15) return reply(res,429,{error:'Please try again later'});
  let size=0;const chunks=[];
  for await (const chunk of req) { size+=chunk.length; if(size>8*1024*1024) return reply(res,413,{error:'Maximum upload is 8 MB'}); chunks.push(chunk); }
  const request = new Request(siteUrl,{method:'POST',headers:{'Content-Type':req.headers['content-type'] || ''},body:Buffer.concat(chunks)});
  let form; try { form=await request.formData(); } catch { return reply(res,400,{error:'Invalid form'}); }
  if(form.get('bot-field')) return reply(res,200,{ok:true});
  const name=form.get('form-name'); const fields=required[name];
  if(!fields) return reply(res,400,{error:'Unknown form'});
  const data={}; for (const [key,value] of form) if(typeof value==='string') data[key]=value.slice(0,20000);
  if(fields.some(key=>!data[key]?.trim()) || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email)) return reply(res,400,{error:'Missing or invalid fields'});
  const attachments=[];
  if(name==='career-application') {
    const file=form.get('resume');
    if(!file || !file.size || file.size>5*1024*1024 || !/\.(pdf|doc|docx)$/i.test(file.name)) return reply(res,400,{error:'Upload a PDF, DOC, or DOCX under 5 MB'});
    const filename=path.basename(file.name).replace(/[^a-zA-Z0-9._-]/g,'_');
    attachments.push({filename,content:Buffer.from(await file.arrayBuffer()).toString('base64')});
    data.resume=`Attached: ${filename}`;
  }
  if(!process.env.RESEND_API_KEY || !process.env.SHINY_EMAIL_FROM) return reply(res,503,{error:'Email service unavailable'});
  const id=crypto.randomUUID();
  await fs.mkdir(dataDir,{recursive:true,mode:0o700});
  const record=path.join(dataDir,`${id}.json`);
  await fs.writeFile(record,JSON.stringify({id,form:name,createdAt:new Date().toISOString(),data,status:'pending'}),{mode:0o600});
  const email=renderEmail(name,data,siteUrl);
  const sent=await fetch('https://api.resend.com/emails',{method:'POST',headers:{Authorization:`Bearer ${process.env.RESEND_API_KEY}`,'Content-Type':'application/json','Idempotency-Key':id},body:JSON.stringify({from:process.env.SHINY_EMAIL_FROM,to:[process.env.SHINY_EMAIL_TO || 'xapollon430@gmail.com'],subject:email.subject,html:email.html,text:email.text,reply_to:email.replyTo,attachments}),signal:AbortSignal.timeout(15000)});
  if(!sent.ok) { console.error(`Email rejected: ${sent.status}, submission ${id}`); return reply(res,502,{error:'Email delivery failed'}); }
  const result=await sent.json();
  await fs.writeFile(record,JSON.stringify({id,form:name,createdAt:new Date().toISOString(),data,status:'sent',emailId:result.id}),{mode:0o600});
  console.log(`Sent ${name}: ${result.id}`); reply(res,200,{ok:true,id});
}
const server=http.createServer(async(req,res)=>{
  try {
    res.setHeader('X-Content-Type-Options','nosniff');res.setHeader('Referrer-Policy','strict-origin-when-cross-origin');
    if(req.method==='POST') return await submit(req,res);
    if(!['GET','HEAD'].includes(req.method)) return reply(res,405,{error:'Method not allowed'});
    let pathname=decodeURIComponent(new URL(req.url,siteUrl).pathname);
    const redirect=redirects.get(pathname) || redirects.get(pathname.endsWith('/') ? pathname : pathname+'/');
    if(redirect) {
      if(redirect.status===410) {
        const body=await fs.readFile(path.join(root,'retired.html'));
        res.writeHead(410,{'Content-Type':'text/html; charset=utf-8','Content-Length':body.length,'X-Robots-Tag':'noindex','Cache-Control':'no-cache'});
        return res.end(req.method==='HEAD'?undefined:body);
      }
      const target=new URL(redirect.to,siteUrl);
      for(const [key,value] of new URL(req.url,siteUrl).searchParams) if(!target.searchParams.has(key)) target.searchParams.append(key,value);
      const location=redirect.to.startsWith('/') ? target.pathname+target.search+target.hash : target.href;
      res.writeHead(redirect.status,{Location:location}); return res.end();
    }
    if(pathname.split('/').some(part=>part.startsWith('.'))) return reply(res,404,{error:'Not found'});
    let file=path.resolve(root,'.'+pathname);
    if(!file.startsWith(root+path.sep) && file!==root) return reply(res,403,{error:'Forbidden'});
    let status=200;
    try { if((await fs.stat(file)).isDirectory()) file=path.join(file,'index.html'); await fs.access(file); }
    catch { file=path.join(root,'404.html');status=404; }
    const body=await fs.readFile(file);res.writeHead(status,{'Content-Type':mime[path.extname(file)] || 'application/octet-stream','Content-Length':body.length,'Cache-Control':file.endsWith('.html')?'no-cache':'public, max-age=3600'});res.end(req.method==='HEAD'?undefined:body);
  } catch(error) { console.error(error.message); if(!res.headersSent) reply(res,500,{error:'Request failed'}); else res.end(); }
});
server.listen(Number(process.env.PORT || 8000),'127.0.0.1',()=>console.log('Shiny listening on port '+(process.env.PORT || 8000)));
