import React, { useEffect } from "react";
import { useState } from "react";
import { Credentials, User } from "../Types";
import { useNavigate } from "react-router-dom";
import { fetchUserById, logIn } from "../Api";
import { tokenStatus } from "../Api";

export const useAuthenticateUser = () => {
	const [isLoading, setIsLoading] = useState(false);
	const [user, setUser] = useState<User | null>(null);
	const [error, setError] = useState<string | null>(null);

	const navigate = useNavigate();

	useEffect(() => {
		if (user) {
			navigate("/home");
		} else {
			if (window.location.pathname === "/signup") {
				navigate("/signup");
			} else {
				navigate("/login");
			}
		}
	}, [user]);

	const authenticate = async (credentials: Credentials): Promise<void> => {
		if (!user) {
			try {
				setIsLoading(true);
				setError(null);

				const tokens = await logIn(credentials);
				localStorage.setItem("token", tokens.access_token);

				if (tokens.user_id) {
					const user = await fetchUserById(tokens.user_id);
					setUser(user);
				} else {
					setError(tokens.message!.split(".")[0] + ".");
					setUser(null);
				}
			} catch (error) {
				setError(error as string);
			} finally {
				setIsLoading(false);
			}
		}
	};

	const validateToken = async () => {
		try {
			const existingToken = localStorage.getItem("token");
			if (existingToken) {
				const response = await tokenStatus(existingToken);

				const { message } = response;
				if (message) throw new Error("Invalid token");

				const user = await fetchUserById(response.id);
				setUser(user);
			}
		} catch (error) {
			logout();
		}
	};

	const logout = () => {
		localStorage.removeItem("token");
		setUser(null);
		navigate("/login");
	};

	return { user, isLoading, authenticate, validateToken, logout, error };
};
