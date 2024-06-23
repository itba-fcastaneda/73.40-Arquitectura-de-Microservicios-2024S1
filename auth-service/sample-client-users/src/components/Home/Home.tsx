import React from "react";
import { Card } from "./Card/Card";
import { useFetchZones } from "../../hooks/useFetchZones";
import { Zone } from "../../Types";

interface Props {
	zones?: Zone[];
}

export const Home: React.FC<Props> = (props) => {
	const { zones, error } = useFetchZones();

	return (
		<div className="Box Big">
			<div className="Items">
				<h2>Zones</h2>
				<div className="List">
					{(props.zones ? props.zones : zones).map((u) => {
						return <Card key={u.id} name={u.name} />;
					})}
				</div>
				{error ? <div className="Disconnected">{error}</div> : <></>}
			</div>
		</div>
	);
};
