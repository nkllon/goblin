import { promises as fs } from "node:fs";
import { DataFactory } from "@rdfjs/data-model";
import rdfDataset from "@rdfjs/dataset";
import { Parser as N3Parser, Writer as N3Writer } from "n3";
import Validator from "rdf-validate-shacl";

export type ValidateOptions = {
  dataFormat?: "turtle" | "jsonld"; // currently supporting turtle best
  shapesFormat?: "turtle";
};

function guessFormat(path: string): "turtle" | "jsonld" {
  const p = path.toLowerCase();
  if (p.endsWith(".ttl")) return "turtle";
  if (p.endsWith(".json") || p.endsWith(".jsonld")) return "jsonld";
  return "turtle";
}

async function parseTurtleToDataset(turtle: string) {
  const parser = new N3Parser({ format: "text/turtle" });
  const quads: any[] = parser.parse(turtle) as any[];
  const dataset = rdfDataset.dataset();
  for (const q of quads) {
    dataset.add(rdfDataset.quad(q.subject, q.predicate, q.object, q.graph));
  }
  return dataset;
}

export async function validate(
  dataPath: string,
  shapesPath: string,
  options: ValidateOptions = {}
): Promise<{ conforms: boolean; reportTurtle: string }> {
  const dataFormat = options.dataFormat ?? guessFormat(dataPath);
  const shapesFormat = options.shapesFormat ?? "turtle";

  if (dataFormat !== "turtle") {
    throw new Error(
      `Unsupported data format '${dataFormat}' in JS validator yet; please provide Turtle (.ttl).`
    );
  }
  if (shapesFormat !== "turtle") {
    throw new Error(`Unsupported shapes format '${shapesFormat}', expected 'turtle'.`);
  }

  const [dataTtl, shapesTtl] = await Promise.all([
    fs.readFile(dataPath, "utf8"),
    fs.readFile(shapesPath, "utf8"),
  ]);

  const dataDataset = await parseTurtleToDataset(dataTtl);
  const shapesDataset = await parseTurtleToDataset(shapesTtl);

  const validator = new Validator(shapesDataset, { factory: DataFactory });
  const report = await validator.validate(dataDataset);

  const writer = new N3Writer({ format: "text/turtle" });
  const reportDataset = report.dataset;
  for (const quad of reportDataset as any) {
    writer.addQuad(quad as any);
  }
  const reportTurtle = await new Promise<string>((resolve, reject) => {
    writer.end((err: Error | null, result?: string) => {
      if (err) reject(err);
      else resolve(result ?? "");
    });
  });

  return { conforms: report.conforms, reportTurtle };
}
