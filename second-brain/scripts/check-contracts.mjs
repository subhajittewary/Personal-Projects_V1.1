import { readdir, readFile } from "node:fs/promises";
import { join } from "node:path";

const directory = new URL("../contracts/json-schema/", import.meta.url);
const names = (await readdir(directory)).filter((name) => name.endsWith(".json"));
if (names.length === 0) throw new Error("No JSON Schema contracts found.");

for (const name of names) {
  const schema = JSON.parse(await readFile(new URL(name, directory), "utf8"));
  if (!schema.$id?.includes("/v1")) throw new Error(`${name} requires a versioned $id.`);
  if (schema.type !== "object") throw new Error(`${name} must define an object contract.`);
  console.log(`validated ${join("contracts/json-schema", name)}`);
}
