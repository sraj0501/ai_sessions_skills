/**
 * ai-session-skills capture plugin for OpenCode.
 *
 * OpenCode has no shell-command hook config, so capture goes through the
 * plugin API instead. Installed by `tool/install.sh`, which copies this file
 * to ~/.config/opencode/plugin/ and substitutes __TOOL_DIR__.
 *
 * Both `tool.execute.before` and `tool.execute.after` are implemented because
 * `after` is not reliably triggered in all OpenCode versions
 * (anomalyco/opencode#25918). Double capture is harmless: identical actions
 * collapse to one signature, so the second event is dropped by the dedupe.
 */

const TOOL_DIR = "__TOOL_DIR__";
const CAPTURE = `${TOOL_DIR}/bin/hook-capture.sh`;
const SESSION = `${TOOL_DIR}/bin/hook-session.sh`;

/** Fire and forget: never await, never throw into OpenCode's tool loop. */
function run(script, args, stdin) {
  try {
    if (typeof Bun !== "undefined" && Bun.spawn) {
      const child = Bun.spawn([script, ...args], {
        stdin: stdin === undefined ? "ignore" : "pipe",
        stdout: "ignore",
        stderr: "ignore",
      });
      if (stdin !== undefined) {
        child.stdin.write(stdin);
        child.stdin.end();
      }
      child.unref?.();
      return;
    }
  } catch {
    /* fall through to node */
  }
  try {
    // eslint-disable-next-line @typescript-eslint/no-var-requires
    const { spawn } = require("node:child_process");
    const child = spawn(script, args, {
      stdio: [stdin === undefined ? "ignore" : "pipe", "ignore", "ignore"],
      detached: true,
    });
    if (stdin !== undefined) {
      child.stdin.write(stdin);
      child.stdin.end();
    }
    child.unref();
  } catch {
    /* capture must never break the session */
  }
}

function capture(tool, args, sessionID, ok) {
  if (!tool || !args) return;
  run(CAPTURE, ["opencode"], JSON.stringify({
    hook_event_name: "PostToolUse",
    tool_name: tool,
    tool_input: args,
    session_id: sessionID || "",
    cwd: process.env.OPENCODE_PROJECT_DIR || process.cwd(),
    tool_response: { success: ok !== false },
  }));
}

export const AiSessionSkills = async () => {
  run(SESSION, ["start", "opencode"]);
  return {
    "tool.execute.before": async (input, output) => {
      capture(input?.tool, output?.args ?? input?.args, input?.sessionID, true);
    },
    "tool.execute.after": async (input, output) => {
      const failed = typeof output?.output === "string" &&
        /^(error|Error:)/.test(output.output.trim());
      capture(input?.tool, input?.args, input?.sessionID, !failed);
    },
    event: async ({ event }) => {
      if (event?.type === "session.idle") run(SESSION, ["end", "opencode"]);
    },
  };
};

export default AiSessionSkills;
