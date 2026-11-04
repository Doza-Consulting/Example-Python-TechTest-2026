import { useEffect, useState } from "react";

import { getHealth } from "../api";

export function HealthBadge() {
  const [healthy, setHealthy] = useState<boolean | null>(null);

  useEffect(() => {
    getHealth()
      .then((h) => setHealthy(h.status === "ok"))
      .catch(() => setHealthy(false));
  }, []);

  return (
    <span className={`status ${healthy === null ? "" : healthy ? "up" : "down"}`}>
      API {healthy === null ? "checking…" : healthy ? "online" : "offline"}
    </span>
  );
}
