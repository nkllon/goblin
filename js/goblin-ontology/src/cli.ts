#!/usr/bin/env node
import { argv, exit } from "node:process";
import { validate } from "./validate.js";

function usage(): string {
  return [
    "Usage: goblin-validate <data.ttl> --shapes <shapes.ttl>",
    "",
    "Validate a Turtle data graph against Goblin SHACL shapes.",
  ].join("\n");
}

async function main(): Promise<number> {
  const args = argv.slice(2);
  if (args.length < 1) {
    console.error(usage());
    return 2;
  }
  const dataPath = args[0];
  const shapesFlagIdx = args.findIndex((a) => a === "--shapes");
  if (shapesFlagIdx === -1 || shapesFlagIdx === args.length - 1) {
    console.error("Missing --shapes <file>.");
    console.error(usage());
    return 2;
  }
  const shapesPath = args[shapesFlagIdx + 1];

  try {
    const { conforms, reportTurtle } = await validate(dataPath, shapesPath, {
      dataFormat: "turtle",
      shapesFormat: "turtle",
    });
    console.log(reportTurtle.trim());
    return conforms ? 0 : 1;
  } catch (err) {
    console.error(String(err));
    return 3;
  }
}

main().then((code) => exit(code));
