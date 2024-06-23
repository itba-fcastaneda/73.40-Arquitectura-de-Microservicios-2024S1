import React, { useEffect } from "react";
import { LogIn } from "./components/LogIn/LogIn";
import { useIsConnected } from "./hooks/useIsConnected";
import { useAuthenticateUser } from "./hooks/useAuthenticateUser";
import { Route, Routes } from "react-router";
import { SignUp } from "./components/SignUp/SignUp";
import { Home } from "./components/Home/Home";
import { Button } from "antd";

function App() {
	const { user, validateToken, logout } = useAuthenticateUser();
	const connection = useIsConnected();

	useEffect(() => {
		validateToken();
	}, []);

	return (
		<div className="App">
			<Routes>
				<Route path="/login" element={!user ? <LogIn /> : <Home />} />
				<Route path="/signup" element={<SignUp />} />
				<Route path="/home" element={!user ? <Home /> : <LogIn />} />
				<Route path="/" element={!user ? <LogIn /> : <Home />} />
			</Routes>
			<div className="FloatingStatus">{connection}</div>
			<div className="LogoutButton">
				{
					<Button
						onClick={() => logout()}
						disabled={!!!localStorage.getItem("token")}
					>
						Logout
					</Button>
				}
			</div>
		</div>
	);
}

export default App;
