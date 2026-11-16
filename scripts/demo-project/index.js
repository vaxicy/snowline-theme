// Snowline Theme — one snow line, six cuts
import { readFile } from 'node:fs/promises';

const SNOWLINE = {
  navy: '#17293D',
  steel: '#94B4C1',
  glacier: '#35609A',
  tundra: '#7C8266',
  frostbell: '#898AC4',
  icefall: '#97A3B0',
  frostpine: '#319798',
  snow: '#F8FAFC',
};

export class Snowline {
  constructor(line = 'North ridge') {
    this.line = line;
    this.palette = SNOWLINE;
    this.cuts = Object.keys(SNOWLINE).filter((name) => name !== 'snow');
  }

  /** Blend two cuts into one colder shade. */
  blend(from, to, ratio = 0.5) {
    const parse = (hex) =>
      [1, 3, 5].map((i) => parseInt(hex.slice(i, i + 2), 16));
    const [a, b] = [parse(from), parse(to)];
    const channel = (value, i) =>
      Math.round(value * (1 - ratio) + b[i] * ratio);
    const toHex = (value) => value.toString(16).padStart(2, '0');
    return '#' + a.map(channel).map(toHex).join('');
  }

  async readLine(file) {
    const content = await readFile(file, 'utf8');
    const layers = content.split('\n').filter(Boolean);
    return {
      line: this.line,
      cuts: this.cuts.length,
      layers: layers.length,
      content,
    };
  }
}

const snowline = new Snowline();
const shade = snowline.blend(SNOWLINE.navy, SNOWLINE.steel);

console.log(`coldest shade: ${shade}`);
