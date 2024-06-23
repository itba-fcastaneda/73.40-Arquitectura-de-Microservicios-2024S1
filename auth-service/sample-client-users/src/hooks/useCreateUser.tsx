import React from "react";
import { useState } from "react";
import { Credentials } from "../Types";
import { createUser as createUserAPI } from "../Api";
import { useAuthenticateUser } from "./useAuthenticateUser";

export const useCreateUser = () => {
	const [isLoading, setIsLoading] = useState(false);
	const [error, setError] = useState<string | null>(null);
	const { authenticate } = useAuthenticateUser();

	const createUser = async (credentials: Credentials): Promise<void> => {
		try {
			setIsLoading(true);
			setError(null);

			const createResponse = await createUserAPI(credentials);

			if (createResponse.id) {
				authenticate(credentials);
			} else {
				setError(createResponse.message);
			}
		} catch (error) {
			setError(error as string);
		} finally {
			setIsLoading(false);
		}
	};

	return { createUser, isLoading, error };
};
