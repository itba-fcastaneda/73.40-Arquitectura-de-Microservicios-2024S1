export interface Credentials {
	password: string;
	email: string;
	username?: string;
}

export interface Token {
	refresh_token: string;
	access_token: string;
}

export interface User {
	id: number;
	username: string;
	email: string;
	created_date?: Date;
}

export interface Zone {
	id: number;
	name: string;
}
