import React from "react";
import { Avatar, Button } from "antd";

interface Props {
	name: string;
}

export const Card: React.FC<Props> = ({ name }) => {
	return (
		<div className="Card">
			<Avatar size="large">{name.slice(0, 1).toUpperCase()}</Avatar>
			{name}
			📍
		</div>
	);
};
