import path from "node:path";
import { fileURLToPath } from "node:url";
import { createEnv } from "@t3-oss/env-core";
import dotenv from "dotenv";
import { z } from "zod";

const dirname = path.dirname(fileURLToPath(import.meta.url));
dotenv.config({ path: path.resolve(dirname, "../../.env") });
dotenv.config({ path: path.resolve(dirname, "../../.env.local") });

export const env = createEnv({
	server: {
		CI: z.coerce.boolean().default(false),
		PORT: z.coerce.number().default(3000),
		APP_URL: z.url().optional(),
	},
	runtimeEnv: process.env,
	emptyStringAsUndefined: true,
});
