import { Axios, AxiosError } from "axios";
import { Credentials, Token, User, Zone } from "./Types";

const instance = new Axios({
	baseURL: "http://127.0.0.1:5000/",
	headers: {
		accept: "application/json",
		"Content-Type": "application/json",
	},
});

instance.interceptors.response.use(
	(response) => {
		return JSON.parse(response.data);
	},
	(error) => {
		const err = error as AxiosError;
		return Promise.reject(err);
	}
);

instance.interceptors.request.use((request) => {
	request.data = JSON.stringify(request.data);
	return request;
});

//Ping
export const ping = () => {
	return instance.get("ping");
};

//Users
export const createUser = (
	credentials: Credentials
): Promise<{ id?: string; message: string }> => {
	return instance.post("users", credentials);
};

export const fetchUsers = (): Promise<User[]> => {
	return instance.get("users");
};

export const fetchUserById = (id: number): Promise<User> => {
	return instance.get("users/" + id);
};

//Auth
export const logIn = (
	credentials: Credentials
): Promise<Token & Partial<{ message: string; user_id: number }>> => {
	return instance.post("auth/login", credentials);
};

export const tokenStatus = (
	token: string
): Promise<User & { message?: string }> => {
	return instance.get("auth/status", {
		headers: { Authorization: `Bearer ${token}` },
	});
};

//Zones
export const fetchZones = (): Promise<Zone[]> => {
	return instance.get("zones");
};
