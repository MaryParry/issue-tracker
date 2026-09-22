import { test as base } from "@playwright/test";
import { AuthPage } from "../pages/auth.page";
import { closeDb, deleteUserByEmail, getUser } from "./db";

export interface TestUser {
	name: string;
	email: string;
	password: string;
}

interface CustomFixtures {
	authPage: AuthPage;
	testUser: TestUser;
}

interface CustomWorkerFixtures {
	// biome-ignore lint/suspicious/noConfusingVoidType: Playwright fixture without value
	dbTeardown: void;
}

export const test = base.extend<CustomFixtures, CustomWorkerFixtures>({
	authPage: async ({ page }, use) => {
		await use(new AuthPage(page));
	},

	// biome-ignore lint/correctness/noEmptyPattern: Playwright fixture syntax requires empty destructuring pattern
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

	// Worker teardown: close DB connection pool after all tests in the worker complete
	dbTeardown: [
		// biome-ignore lint/correctness/noEmptyPattern: Playwright fixture syntax requires empty destructuring pattern
		async ({}, use) => {
			await use();
			await closeDb();
		},
		{ scope: "worker", auto: true },
	],
});

export { expect } from "@playwright/test";
export { closeDb, deleteUserByEmail, getUser };
