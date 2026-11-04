import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";

import { App } from "./App";

beforeEach(() => {
  vi.stubGlobal(
    "fetch",
    vi.fn().mockImplementation(async (url: string) => ({
      ok: true,
      status: 200,
      json: async () => (url.endsWith("/health") ? { status: "ok" } : { data: [] }),
    }))
  );
});

afterEach(() => vi.unstubAllGlobals());

describe("App", () => {
  it("navigates to the About page", async () => {
    render(
      <MemoryRouter initialEntries={["/"]}>
        <App />
      </MemoryRouter>
    );

    await userEvent.click(screen.getByRole("link", { name: "About" }));

    expect(screen.getByRole("heading", { name: /about escape queue/i })).toBeInTheDocument();
  });

  it("shows the API as online when health passes", async () => {
    render(
      <MemoryRouter>
        <App />
      </MemoryRouter>
    );

    expect(await screen.findByText(/api online/i)).toBeInTheDocument();
  });
});
