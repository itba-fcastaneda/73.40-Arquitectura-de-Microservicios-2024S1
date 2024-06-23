import React, { useEffect } from "react";
import { useState } from "react";
import { ping } from "../Api";

export const useIsConnected = () => {
	const [connected, setConnected] = useState(false);

	useEffect(() => {
		ping()
			.then(() => {
				setConnected(true);
			})
			.catch(() => {
				setConnected(false);
			});
	}, []);

	return (
		<div>
			{connected ? (
				<p className="Connected">Connected</p>
			) : (
				<p className="Disconnected">Disconnected</p>
			)}
		</div>
	);
};
