import path from "node:path";
import { fileURLToPath } from "node:url";
import { defineConfig, devices } from "@playwright/test";
import dotenv from "dotenv";

const dirname = path.dirname(fileURLToPath(import.meta.url));
dotenv.config({ path: path.resolve(dirname, "../../.env") });

const port = process.env.PORT || 3000;
const baseURL = process.env.APP_URL || `http://localhost:${port}`;

export default defineConfig({
	testDir: "./tests",
	fullyParallel: true,
	forbidOnly: !!process.env.CI,
	retries: process.env.CI ? 2 : 0,
	workers: process.env.CI ? 1 : undefined,
	reporter: [["list"], ["html", { open: "never" }]],
	use: {
		baseURL,
		trace: "on-first-retry",
		screenshot: "only-on-failure",
		video: "retain-on-failure",
	},
	projects: [
		// {
		//   name: "chromium",
		//   use: { ...devices["Desktop Chrome"] },
		// },
		{
			name: "firefox",
			use: { ...devices["Desktop Firefox"] },
		},
		// {
		//   name: "webkit",
		//   use: { ...devices["Desktop Safari"] },
		// },
	],
	webServer: {
		command: "bun dev",
		url: baseURL,
		reuseExistingServer: !process.env.CI,
		cwd: "../../",
		timeout: 120 * 1000,
	},
});
