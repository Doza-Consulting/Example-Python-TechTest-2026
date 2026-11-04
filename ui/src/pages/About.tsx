export function About() {
  return (
    <>
      <h2>About Escape Queue</h2>

      <p>
        Escape Queue is a (fictional) chain of escape room venues. Teams of
        friends, families and colleagues are locked in themed rooms and have
        under an hour to solve puzzles and break out. Each room has its own
        story, difficulty, group size and running time, and every game is
        guided by a game master who watches the team, gives hints and keeps
        everyone safe.
      </p>

      <h3>What this app is for</h3>
      <p>
        This is the company's booking engine. It has two audiences:
      </p>
      <ul>
        <li>
          <strong>Customers</strong> can browse the rooms and see which time
          slots are free. This part is public and shows nothing about other
          people's bookings.
        </li>
        <li>
          <strong>Venue staff</strong> sign in to create, move and cancel
          bookings, and to assign a game master to each session.
        </li>
      </ul>

      <h3>The rules of the business</h3>
      <ul>
        <li>A party must fit the room's minimum and maximum group size.</li>
        <li>A room can only host one game at a time, so bookings must never overlap.</li>
        <li>A session's end time comes from the room's running time.</li>
        <li>Cancelled bookings free the slot up again.</li>
      </ul>

      <p className="note">
        This app is the starting point for a technical assessment. Some
        features are still to be built, so not everything here works yet.
      </p>
    </>
  );
}
