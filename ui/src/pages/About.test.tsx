import { render, screen } from "@testing-library/react";

import { About } from "./About";

describe("About", () => {
  it("explains what the app is for", () => {
    render(<About />);

    expect(screen.getByRole("heading", { name: /about escape queue/i })).toBeInTheDocument();
    expect(screen.getByText(/booking engine/i)).toBeInTheDocument();
  });
});
