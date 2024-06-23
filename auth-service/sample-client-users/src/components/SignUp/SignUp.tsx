import React, { useState } from "react";
import { Button, Input } from "antd";
import { useCreateUser } from "../../hooks/useCreateUser";

export const SignUp = () => {
	const [username, setUsername] = useState("");
	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");
	const [repeatPassword, setRepeatPassword] = useState("");

	const { createUser, isLoading, error } = useCreateUser();

	return (
		<div className="Box Small">
			<div className="Section">
				<img
					alt="logo"
					className="Image"
					src="https://www.seekpng.com/png/full/353-3537757_logo-itba.png"
				/>
				<div className="Section">
					<Input
						type="email"
						placeholder="Email"
						onChange={(ev) => setEmail(ev.target.value)}
					/>
					<Input
						placeholder="Username"
						onChange={(ev) => setUsername(ev.target.value)}
					/>
					<Input.Password
						placeholder="Password"
						onChange={(ev) => setPassword(ev.target.value)}
					/>
					<Input.Password
						placeholder="Repeat password"
						onChange={(ev) => setRepeatPassword(ev.target.value)}
					/>
					<Button
						style={{ width: "100%" }}
						onClick={async () =>
							await createUser({ email, password, username })
						}
						loading={isLoading}
						disabled={
							email === "" ||
							username === "" ||
							password === "" ||
							password !== repeatPassword
						}
					>
						Sign up
					</Button>
					{error ? (
						<div className="Disconnected">{error}</div>
					) : (
						<></>
					)}
				</div>
			</div>
		</div>
	);
};
