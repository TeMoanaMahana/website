import nodemailer from "nodemailer";
import { existsSync, readFileSync } from "node:fs";

// ---------------------------------------------------------------
// Settings you may need to change
// ---------------------------------------------------------------

// Personal Outlook/Hotmail/Live account:  smtp-mail.outlook.com
// Work/organisation Microsoft 365 account: smtp.office365.com
const SMTP_HOST = "smtp-mail.outlook.com";
const SMTP_PORT = 587;

const SUBJECT = "2026 Te Moana Mahana Annual Newsletter";

// While true, the email is ONLY sent to TEST_ADDRESS (your own address).
// Set to false when you are happy with the test and want to send to everyone.
const TEST_MODE = true;

// ---------------------------------------------------------------
// Everything below should not need changing
// ---------------------------------------------------------------

const user = process.env.SMTP_USER;
const pass = process.env.SMTP_PASSWORD;

if (!user || !pass) {
  console.error(
    "Missing SMTP_USER or SMTP_PASSWORD. Create a .env file (see .env.example) " +
      "and run:  node --env-file=.env send.mjs",
  );
  process.exit(1);
}

const HTML_FILE = "./dist/2026.html";
if (!existsSync(HTML_FILE)) {
  console.error(`Can't find ${HTML_FILE}. Run  npm run build  first.`);
  process.exit(1);
}
const html = readFileSync(HTML_FILE, "utf8");

// The "from" address must be the same account you log in with.
const FROM = `Te Moana Mahana <${user}>`;

let recipients;
if (TEST_MODE) {
  recipients = [user]; // sends the test to yourself
  console.log(`TEST MODE: sending only to ${user}`);
} else {
  if (!existsSync("./subscribers.txt")) {
    console.error("Can't find subscribers.txt (one email address per line).");
    process.exit(1);
  }
  recipients = readFileSync("./subscribers.txt", "utf8")
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter((line) => line && !line.startsWith("#"));
  console.log(`Sending to ${recipients.length} subscribers...`);
}

const transporter = nodemailer.createTransport({
  host: SMTP_HOST,
  port: SMTP_PORT,
  requireTLS: true,
  auth: { user, pass },
});

// One separate email per person, so nobody sees anyone else's address.
for (const to of recipients) {
  try {
    await transporter.sendMail({ from: FROM, to, subject: SUBJECT, html });
    console.log("Sent to", to);
  } catch (err) {
    console.log("FAILED for", to, "-", err.message);
  }
}
