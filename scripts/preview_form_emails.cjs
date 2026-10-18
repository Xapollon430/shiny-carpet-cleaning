const {renderEmail} = require('../emails/render.cjs');
const {mkdirSync, writeFileSync} = require('node:fs');
const {resolve} = require('node:path');
const data = {name:'Shiny Website Test',email:'Xapollon430@gmail.com',phone:'7039759099',zip:'22153',service:'Carpet cleaning',details:'TEST ONLY. Two carpeted rooms and pet stains.\nPlease do not schedule service.',topic:'Service question',message:'TEST ONLY. Checking the website email layout. No action needed.',position:'Carpet Cleaning Technician',location:'Springfield',experience:'0',availability:'TEST ONLY. No application or appointment requested.',resume:'https://example.com/test-resume.pdf'};
const directory = resolve(__dirname,'../review-screenshots/emails'); mkdirSync(directory,{recursive:true});
for (const name of ['quote-request','contact-message','career-application']) {
  const rendered = renderEmail(name,data,'http://127.0.0.1:4173');
  writeFileSync(resolve(directory,`${name}.html`),rendered.html);
  console.log(`${name}: ${rendered.subject}`);
}
