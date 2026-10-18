import { cp, mkdir, readdir, readFile, writeFile } from 'node:fs/promises';
import { resolve, join } from 'node:path';
const output = resolve(process.argv[2] || '../shiny-build');
await mkdir(output, { recursive: true });
await cp('dist', output, { recursive: true });
async function rewrite(directory) {
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const path = join(directory, entry.name);
    if (entry.isDirectory()) await rewrite(path);
    else if (path.endsWith('.html')) {
      let html = await readFile(path, 'utf8');
      html = html.replace(/action="\/"/g, 'action="/shiny-carpet-cleaning/_submit"');
      html = html.replace(/((?:href|src|action|poster)=")\/(?!\/|shiny-carpet-cleaning\/)/g, '$1/shiny-carpet-cleaning/');
      await writeFile(path, html);
    }
  }
}
await rewrite(output);

const script = resolve(output, 'assets/site.js');
await writeFile(script, (await readFile(script, 'utf8')).replaceAll('href="/locations/', 'href="/shiny-carpet-cleaning/locations/'));
