import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";
import "../../../matchMedia.mock";

import { Card } from "./Card";

describe("Card Component Test", () => {
	test("Display initial, name and icon", async () => {
		render(<Card name="Belgrano" />);

		expect(screen.getByText("Belgrano📍")).toBeVisible();
		expect(screen.getByText("B")).toBeVisible();
	});
});
