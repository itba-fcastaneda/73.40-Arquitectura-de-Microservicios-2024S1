const mockedUsedNavigate = jest.fn();

jest.mock("react-router-dom", () => ({
	...jest.requireActual("react-router-dom"),
	useNavigate: () => mockedUsedNavigate,
}));

import "../../matchMedia.mock";
import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";
import { Home } from "./Home";

describe("Home View Test", () => {
	test("Display initial, name and icon", async () => {
		render(
			<Home
				zones={[
					{ id: 1, name: "Belgrano" },
					{ id: 2, name: "San Isidro" },
				]}
			/>
		);

		expect(screen.getByText("Zones")).toBeVisible();
		expect(screen.getByText("Belgrano📍")).toBeVisible();
		expect(screen.getByText("San Isidro📍")).toBeVisible();
	});
});
