// The Commons' dated counts, as data, computed at the edge from the
// site's own published files on each request. An agent can cite the
// counts with their sources and the date they were read. Nothing is
// collected about the reader; the function reads only public files
// the site itself serves.
//
// Sources: foundations.json (the findings), site.json (the seven
// acts), layers.json (the acts with their door lines and first steps).

export async function onRequest(context) {
  const { request, env } = context;
  const origin = new URL(request.url).origin;
  const headers = {
    "content-type": "application/json; charset=utf-8",
    "cache-control": "public, max-age=300",
  };
  try {
    const read = async (path) => {
      const res = await env.ASSETS.fetch(new URL(path, origin));
      if (!res.ok) { throw new Error(path); }
      return res.json();
    };
    const foundations = await read("/foundations.json");
    const site = await read("/site.json");
    const body = {
      service: "Topsoil Commons, the dated counts as data",
      read_on: new Date().toISOString().slice(0, 10),
      rule: site.rule,
      foundations_findings: foundations.length,
      acts: site.acts.map((a) => ({
        layer: a.layer,
        act: a.act,
        need: a.need,
        door: a.door,
        first_step: a.first_step,
        see: a.see,
        check: a.check,
      })),
      sources: {
        findings: origin + "/foundations.json",
        acts: origin + "/site.json",
        layers: origin + "/layers.json",
        give: origin + "/api/give",
      },
      honesty: "Counts carry their source and the date they were read. " +
        "A Ground listing past its expiry date is stale; the listings " +
        "themselves stand in the Ground data file named in site.json.",
    };
    return new Response(JSON.stringify(body), { headers });
  } catch (err) {
    return new Response(
      JSON.stringify({ error: "the site's own source files did not answer" }),
      { status: 502, headers });
  }
}
