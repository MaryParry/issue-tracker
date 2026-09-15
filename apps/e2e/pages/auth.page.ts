import type { Locator, Page } from "@playwright/test";

export interface AuthPageNavigateOptions {
	email?: string;
	initialMode?: "signin" | "signup";
	inviteToken?: string;
}

/**
 * Page Object Model for the Authentication page (/auth).
 * Encapsulates element locators and user interactions.
 */
export class AuthPage {
	readonly page: Page;

	// Form inputs
	readonly emailInput: Locator;
	readonly passwordInput: Locator;
	readonly nameInput: Locator;

	// Action buttons
	readonly signInSubmitButton: Locator;
	readonly signUpSubmitButton: Locator;
	readonly toggleSignUpButton: Locator;
	readonly toggleSignInButton: Locator;

	// feedback and alerts
	readonly formError: Locator;

	constructor(page: Page) {
		this.page = page;

		this.emailInput = page.getByRole("textbox", { name: /email/i });
		this.passwordInput = page.getByLabel(/password/i);
		this.nameInput = page.getByRole("textbox", { name: /name/i });

		this.signInSubmitButton = page.getByRole("button", {
			name: "Sign In",
			exact: true,
		});
		this.signUpSubmitButton = page.getByRole("button", {
			name: "Sign Up",
			exact: true,
		});

		this.toggleSignUpButton = page.getByRole("button", {
			name: "Sign up",
			exact: true,
		});
		this.toggleSignInButton = page.getByRole("button", {
			name: "Sign in",
			exact: true,
		});

		this.formError = page.locator(".form-error");
	}

	/**
	 * Navigates to the /auth route with optional query parameters.
	 */
	async goto(options?: AuthPageNavigateOptions): Promise<void> {
		const params = new URLSearchParams();
		if (options?.email) params.set("email", options.email);
		if (options?.initialMode) params.set("initialMode", options.initialMode);
		if (options?.inviteToken) params.set("inviteToken", options.inviteToken);

		const queryString = params.toString();
		const path = queryString ? `/auth?${queryString}` : "/auth";
		await this.page.goto(path);
	}

	/**
	 * Switches the form mode from Sign In to Sign Up.
	 */
	async switchToSignUp(): Promise<void> {
		await this.toggleSignUpButton.click();
	}

	/**
	 * Switches the form mode from Sign Up to Sign In.
	 */
	async switchToSignIn(): Promise<void> {
		await this.toggleSignInButton.click();
	}

	/**
	 * Fills and submits the sign-in form.
	 */
	async signIn(email: string, password: string): Promise<void> {
		await this.emailInput.fill(email);
		await this.passwordInput.fill(password);
		await this.signInSubmitButton.click();
	}

	/**
	 * Fills and submits the sign-up form.
	 */
	async signUp(name: string, email: string, password: string): Promise<void> {
		await this.switchToSignUp();
		await this.nameInput.fill(name);
		await this.emailInput.fill(email);
		await this.passwordInput.fill(password);
		await this.signUpSubmitButton.click();
	}
}
