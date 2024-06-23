import React, { useEffect } from "react";
import { useState } from "react";
import { User, Zone } from "../Types";
import { fetchZones } from "../Api";

export const useFetchZones = () => {
	const [error, setError] = useState<string | null>(null);
	const [zones, setZones] = useState<Zone[]>([]);

	useEffect(() => {
		setError(null);

		fetchZones()
			.then((data) => {
				setZones(data);
			})
			.catch((error) => {
				setError(error as string);
			});
	}, []);

	return { zones, error };
};
