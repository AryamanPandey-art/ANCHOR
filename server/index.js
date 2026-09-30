import express from 'express';
import cors from 'cors';
import { executeTroubleshootingPipeline } from './engine/pipeline.js';
import { getDataSourceReport } from './data/index.js';

const app = express();
const PORT = 3001;

app.use(cors());
app.use(express.json());

// System state
let currentSession = {
  systemStatus: "ONLINE",
  engineMode: "PROOF_CARRYING_GROUNDED",
  contractGuard: "ENFORCED"
};

// Main ANCHOR Diagnosis Pipeline Endpoint
app.post('/api/diagnose', (req, res) => {
  const query = req.body.query !== undefined
    ? req.body.query
    : "My screen isn't rotating automatically.";
  const result = executeTroubleshootingPipeline(query);

  res.json({
    session: currentSession,
    ...result
  });
});

// System session endpoint
app.get('/api/session', (req, res) => {
  res.json(currentSession);
});

// Data source & provenance audit report
app.get('/api/data-audit', (req, res) => {
  res.json(getDataSourceReport());
});

// Quick preset chips
app.get('/api/quick-examples', (req, res) => {
  res.json([
    { label: "+ Screen Rotate", query: "My screen isn't rotating automatically." },
    { label: "+ Touchscreen Lag", query: "My Nexa X1 screen inputs are delayed and the touch responsiveness is laggy." },
    { label: "+ Disable Touch", query: "Touch sensitivity isn't working. Turn it off." },
    { label: "+ Screen Damage", query: "The mobile phone screen is cracked and flashes intermittently." },
    { label: "+ Fingerprint Check", query: "Fingerprint sensor is not recognizing my touch." },
    { label: "+ Disable Rotate", query: "Turn off auto rotate to lock screen." }
  ]);
});


app.listen(PORT, () => {
  console.log(`ANCHOR Engine Backend running on http://localhost:${PORT}`);
});
