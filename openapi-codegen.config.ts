import {
  generateSchemaTypes,
  generateReactQueryComponents,
} from "@openapi-codegen/typescript";
import { defineConfig } from "@openapi-codegen/cli";
export default defineConfig({
  skyline: {
    from: {
      source: "url",
      url: "http://localhost:8000/openapi.json",
    },
    outputDir: "frontend/src/queries/api",
    to: async (context) => {
      const filenamePrefix = "skyline";
      const { schemasFiles } = await generateSchemaTypes(context, {
        filenamePrefix,
      });
      await generateReactQueryComponents(context, {
        filenamePrefix,
        schemasFiles,
      });
    },
  },
});
