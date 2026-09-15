import type { Browser, Page } from "playwright";
import { firefox } from "playwright";
import { afterAll, test as base } from "vitest";
import { AuthPage } from "../pages/auth.page";
import { deleteUserByEmail, getUser } from "./db";

export interface TestUser {
	name: string;
	email: string;
	password: string;
}

interface CustomFixtures {
	page: Page;
	authPage: AuthPage;
	testUser: TestUser;
}

let browser: Browser | null = null;

async function getBrowser(): Promise<Browser> {
	if (!browser) {
		const isHeaded =
			process.env.HEADED === "true" || process.argv.includes("--headed");
		browser = await firefox.launch({ headless: !isHeaded });
	}
	return browser;
}

const extendedTest = base.extend<CustomFixtures>({
	// biome-ignore lint/correctness/noEmptyPattern: Vitest fixture syntax requires empty destructuring pattern
	page: async ({}, use) => {
		const b = await getBrowser();
		const context = await b.newContext({
			baseURL: process.env.APP_URL || "http://localhost:3000",
		});
		const page = await context.newPage();
		await use(page);
		await context.close();
	},

	authPage: async ({ page }, use) => {
		await use(new AuthPage(page));
	},

	// biome-ignore lint/correctness/noEmptyPattern: Vitest fixture syntax requires empty destructuring pattern
	testUser: async ({}, use) => {
		const uid = Math.random().toString(36).slice(2, 8);
		const user: TestUser = {
			name: `Test User ${uid}`,
			email: `test-${uid}@example.com`,
			password: "Password123!",
		};

		await use(user);

		// Teardown: clean up test data from DB after test completes
		await deleteUserByEmail(user.email);
	},
});

export const test = Object.assign(extendedTest, {
	step: async <T>(_title: string, fn: () => Promise<T> | T): Promise<T> => {
		return await fn();
	},
});

afterAll(async () => {
	if (browser) {
		await browser.close();
		browser = null;
	}
});

export { expect } from "@playwright/test";
export { deleteUserByEmail, getUser };
