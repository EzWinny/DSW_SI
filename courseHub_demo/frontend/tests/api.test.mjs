import assert from "node:assert/strict";
import test from "node:test";

import { api } from "../src/api.js";

test("api returns JSON for a GET request without adding a body", async (t) => {
  let request;
  t.mock.method(globalThis, "fetch", async (...args) => {
    request = args;
    return new Response('{"courses":[]}', { status: 200 });
  });

  assert.deepEqual(await api("/courses"), { courses: [] });
  assert.equal(request[1].method, "GET");
  assert.deepEqual(request[1].headers, {});
  assert.equal(request[1].body, undefined);
});

test("api sends JSON request details and returns the response body", async (t) => {
  let request;
  t.mock.method(globalThis, "fetch", async (...args) => {
    request = args;
    return new Response('{"message":"created"}', { status: 201 });
  });

  const body = { student_id: "22000002" };
  const result = await api("/enrollments", { method: "POST", body });

  assert.deepEqual(result, { message: "created" });
  assert.equal(request[0], "http://127.0.0.1:8000/enrollments");
  assert.equal(request[1].method, "POST");
  assert.equal(request[1].headers["Content-Type"], "application/json");
  assert.equal(request[1].body, JSON.stringify(body));
});

test("api returns null for a successful 204 response", async (t) => {
  t.mock.method(globalThis, "fetch", async () => new Response(null, { status: 204 }));

  assert.equal(await api("/enrollments/22000002/RACE-01", { method: "DELETE" }), null);
});

test("api exposes the status and detail for an HTTP error", async (t) => {
  t.mock.method(globalThis, "fetch", async () =>
    new Response('{"detail":"Class is full"}', { status: 409 }),
  );

  await assert.rejects(
    api("/enrollments"),
    (error) => {
      assert.equal(error.status, 409);
      assert.equal(error.message, "HTTP 409: Class is full");
      return true;
    },
  );
});

test("api joins validation messages from an array detail", async (t) => {
  t.mock.method(globalThis, "fetch", async () =>
    new Response(
      '{"detail":[{"msg":"Field required"},{"msg":"Invalid value"}]}',
      { status: 422 },
    ),
  );

  await assert.rejects(
    api("/enrollments"),
    (error) => error.message === "HTTP 422: Field required; Invalid value",
  );
});

test("api uses a fallback message for unrecognized error details", async (t) => {
  t.mock.method(globalThis, "fetch", async () =>
    new Response('{"detail":{"message":"unexpected"}}', { status: 500 }),
  );

  await assert.rejects(
    api("/courses"),
    (error) => error.message === "HTTP 500: Yêu cầu không thành công.",
  );
});

test("api reports non-JSON responses", async (t) => {
  t.mock.method(globalThis, "fetch", async () =>
    new Response("not JSON", { status: 200 }),
  );

  await assert.rejects(
    api("/courses"),
    (error) => error.message === "HTTP 200: phản hồi không phải JSON.",
  );
});

test("api translates network errors and preserves abort errors", async (t) => {
  const abortError = new Error("Request cancelled");
  abortError.name = "AbortError";
  let calls = 0;
  t.mock.method(globalThis, "fetch", async () => {
    calls += 1;
    throw calls === 1 ? new Error("Network unavailable") : abortError;
  });

  await assert.rejects(
    api("/courses"),
    (error) =>
      error.message ===
      "Không nhận được phản hồi API. Kiểm tra Backend/CORS và tải lại dữ liệu trước khi gửi lại thao tác.",
  );
  await assert.rejects(api("/courses"), (error) => error === abortError);
});
