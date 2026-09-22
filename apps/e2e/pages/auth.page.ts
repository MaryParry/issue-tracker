import type { Page } from "@playwright/test";

export interface AuthPageNavigateOptions {
	email?: string;
	initialMode?: "signin" | "signup";
	inviteToken?: string;
}

export class AuthPage {
	constructor(readonly page: Page) {}

	// Form inputs
	get emailInput() {
		return this.page.getByRole("textbox", { name: /email/i });
	}
	get passwordInput() {
		return this.page.getByLabel(/password/i);
	}
	get nameInput() {
		return this.page.getByRole("textbox", { name: /name/i });
	}

	// Action buttons
	get signInSubmitButton() {
		return this.page.getByRole("button", { name: "Sign In", exact: true });
	}
	get signUpSubmitButton() {
		return this.page.getByRole("button", { name: "Sign Up", exact: true });
	}
	get toggleSignUpButton() {
		return this.page.getByRole("button", { name: "Sign up", exact: true });
	}
	get toggleSignInButton() {
		return this.page.getByRole("button", { name: "Sign in", exact: true });
	}

	// Feedback & alerts
	get formError() {
		return this.page.locator(".form-error");
	}

	async goto(options?: AuthPageNavigateOptions): Promise<void> {
		const params = new URLSearchParams();
		if (options?.email) params.set("email", options.email);
		if (options?.initialMode) params.set("initialMode", options.initialMode);
		if (options?.inviteToken) params.set("inviteToken", options.inviteToken);

		const queryString = params.toString();
		await this.page.goto(queryString ? `/auth?${queryString}` : "/auth");
	}

	async switchToSignUp(): Promise<void> {
		await this.toggleSignUpButton.click();
	}

	async switchToSignIn(): Promise<void> {
		await this.toggleSignInButton.click();
	}

	async signIn(email: string, password: string): Promise<void> {
		await this.emailInput.fill(email);
		await this.passwordInput.fill(password);
		await this.signInSubmitButton.click();
	}

	async signUp(name: string, email: string, password: string): Promise<void> {
		await this.switchToSignUp();
		await this.nameInput.fill(name);
		await this.emailInput.fill(email);
		await this.passwordInput.fill(password);
		await this.signUpSubmitButton.click();
	}
}
