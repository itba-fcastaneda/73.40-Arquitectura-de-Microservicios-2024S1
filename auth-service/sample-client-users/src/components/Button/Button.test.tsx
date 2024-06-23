import "../../matchMedia.mock";
import "@testing-library/jest-dom";
import userEvent from "@testing-library/user-event";
import { render, screen } from "@testing-library/react";
import { Button } from "antd";

describe("Button Component Test", () => {
	test("Display button label and clicked", async () => {
		const onClick = jest.fn();

		render(<Button onClick={() => onClick()}>Button</Button>);

		expect(screen.getByText("Button")).toBeVisible();
		await userEvent.click(screen.getByText("Button"));
		expect(onClick).toBeCalled();
	});
});
