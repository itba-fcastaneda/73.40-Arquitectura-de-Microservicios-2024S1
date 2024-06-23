import React, { useState } from "react";
import { Button, Input } from "antd";
import { useAuthenticateUser } from "../../hooks/useAuthenticateUser";

export const LogIn = () => {
	const { isLoading, error, authenticate } = useAuthenticateUser();
	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");

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
						placeholder="User"
						onChange={(ev) => setEmail(ev.target.value)}
					/>
					<Input.Password
						placeholder="Password"
						onChange={(ev) => setPassword(ev.target.value)}
					/>
					<Button
						style={{ width: "100%" }}
						onClick={async () =>
							await authenticate({ email, password })
						}
						loading={isLoading}
					>
						Log in
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
