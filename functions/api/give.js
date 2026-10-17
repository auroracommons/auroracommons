// Giving, staged and shut until a fiscal host is appointed.
//
// The charter rule stands above this code: money moves only through a
// fiscal host, never to a personal account, and no host is appointed
// today. So this endpoint takes no payment and names no account. It
// answers, in the open, exactly what will open and when.
//
// Activation is one configuration value, set in the Pages project the
// day a host is appointed: FISCAL_HOST_GIVE_URL, the host's own hosted
// giving page. With it set, this endpoint sends the visitor straight
// to the host's page, where the host receives and holds the money.
// Nothing else changes: no build, no new code, no personal account
// anywhere in the path.

export async function onRequest(context) {
  const { env } = context;
  const host = env.FISCAL_HOST_GIVE_URL;
  if (host) {
    return new Response(null, {
      status: 302,
      headers: { location: host, "cache-control": "no-store" },
    });
  }
  const body = {
    status: "not_open",
    why: "Topsoil Commons has no fiscal host appointed. Money moves " +
      "only through a fiscal host, never to a personal account, so " +
      "this door stays shut until a host is appointed.",
    opens_when: "The day a fiscal host is appointed, this endpoint " +
      "is pointed at the host's hosted giving page by one " +
      "configuration value. Activation is a setting, not a build.",
    flow: [
      "A person chooses an amount on the host's hosted giving page.",
      "The host receives the money and holds it. No Commons account " +
        "and no personal account touches it.",
      "The gift enters the public ledger within seven days of the " +
        "host's statement, under the published funds rules.",
      "Money buys nothing but the work itself: no votes, no " +
        "standing, no placement.",
    ],
    rules: "https://topsoilcommons.org/funds",
  };
  return new Response(JSON.stringify(body), {
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store",
    },
  });
}
