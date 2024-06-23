const mockedUsedNavigate = jest.fn();

jest.mock("react-router-dom", () => ({
	...jest.requireActual("react-router-dom"),
	useNavigate: () => mockedUsedNavigate,
}));

import "../matchMedia.mock";
import { act, renderHook } from "@testing-library/react";
import { useAuthenticateUser } from "./useAuthenticateUser";

describe("UseAuthenticateUser Hook Test", () => {
	afterEach(() => {
		localStorage.removeItem("token");
	});

	test("Hook initial state", async () => {
		const { result } = renderHook(() => useAuthenticateUser());
		expect(result.current.isLoading).toBeFalsy();
		expect(result.current.error).toBeNull();
	});

	test("Hook fetch state - Authenticate function - Promise not resolved", async () => {
		const { result } = renderHook(() => useAuthenticateUser());

		act(() => {
			result.current.authenticate({
				email: "martin@gmail.com",
				password: "password1234",
			});
		});

		expect(result.current.isLoading).toBeTruthy();
		expect(result.current.error).toBeNull();
	});

	test("Hook fetch state - Authenticate function - Promise success", async () => {
		const { result } = renderHook(() => useAuthenticateUser());

		await act(async () => {
			await result.current.authenticate({
				email: "martin@gmail.com",
				password: "password1234",
			});
		});

		expect(localStorage.getItem("token")).not.toBeNull();
		expect(result.current.isLoading).toBeFalsy();
		expect(result.current.error).not.toBeNull();
	});

	test("Hook fetch state - Authenticate function - Promise failed", async () => {
		const { result } = renderHook(() => useAuthenticateUser());

		await act(async () => {
			await result.current.authenticate({
				email: "notExistingUser",
				password: "notExistingUser",
			});
		});

		expect(localStorage.getItem("token")).toBe("undefined");
		expect(result.current.isLoading).toBeFalsy();
		expect(result.current.error).not.toBeNull();
	});
});
