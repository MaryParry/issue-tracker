import { Pool } from "pg";

const pool = new Pool({
	connectionString:
		process.env.DATABASE_URL ||
		"postgres://postgres:postgres@localhost:5432/issue_tracker",
});

export async function deleteUserByEmail(email: string): Promise<void> {
	await pool.query('DELETE FROM "user" WHERE email = $1', [
		email.toLowerCase(),
	]);
}

export async function getUser(email: string) {
	const res = await pool.query('SELECT * FROM "user" WHERE email = $1', [
		email.toLowerCase(),
	]);
	return res.rows[0] ?? null;
}
