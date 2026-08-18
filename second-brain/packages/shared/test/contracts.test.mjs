import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";

const schemaDir = new URL("../../../contracts/json-schema/", import.meta.url);

for (const name of ["error-envelope.v1.json", "document.v1.json", "chat-event.v1.json"]) {
  test(`${name} declares a versioned canonical schema`, async () => {
    const content = await readFile(new URL(name, schemaDir), "utf8");
    const schema = JSON.parse(content);
    assert.match(schema.$id, /\/v1$/);
    assert.equal(schema.additionalProperties, false);
  });
}
