import { render, screen } from "@testing-library/react";

import { Rooms } from "./Rooms";

/**
 * Pattern for testing components that call the API: stub `fetch` rather
 * than hitting a real server.
 */
function mockFetch(response: { ok: boolean; status?: number; body?: unknown }) {
  vi.stubGlobal(
    "fetch",
    vi.fn().mockResolvedValue({
      ok: response.ok,
      status: response.status ?? 200,
      json: async () => response.body,
    })
  );
}

afterEach(() => vi.unstubAllGlobals());

describe("Rooms", () => {
  it("renders a card for each room", async () => {
    mockFetch({
      ok: true,
      body: {
        data: [
          {
            id: "1",
            name: "The Vault",
            theme: "Heist",
            minPartySize: 2,
            maxPartySize: 6,
            durationMinutes: 60,
          },
        ],
      },
    });

    render(<Rooms />);

    expect(await screen.findByRole("heading", { name: "The Vault" })).toBeInTheDocument();
    expect(screen.getByText(/2–6 players/)).toBeInTheDocument();
  });

  it("shows an error when the API fails", async () => {
    mockFetch({ ok: false, status: 500 });

    render(<Rooms />);

    expect(await screen.findByText(/could not load rooms/i)).toBeInTheDocument();
  });
});
