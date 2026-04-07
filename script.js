/* ============================================================
   Roku Intelligence Center — script.js
   ============================================================ */

// ── STATE ─────────────────────────────────────────────────────
const state = {
  activeTab: 'account-plan',
  activeAccount: 'all',
  currentYear: 2025,
  accounts: {
    wbd: {
      name: 'Warner Bros. Discovery',
      short: 'WBD',
      vertical: 'Entertainment',
      subVertical: 'Streaming / Broadcast',
      reminder: 'Q3 review scheduled July 15 — prepare pacing update',
      tags: ['Brand Awareness', 'Reach 18–49', 'CTV Priority', 'Upfront Deal'],
      primaryKpiLabel: 'Q2 Revenue Goal',
      primaryKpiValue: '$4.2M · 78% to Goal',
      pacing: {
        quarterLabel: 'Q2 2025',
        quarterBooked: 3276000,
        quarterGoal: 4200000,
        pctToGoal: 78,
        revenueAtRisk: 420000,
        note: 'Two DIO campaigns ending June 28 without renewal confirmation. Priority: close PMP renewal before EOM.'
      },
      sfOpps: [
        { name: 'WBD · Q3 DIO Renewal', stage: 'Proposal Sent', priority: 'high', url: 'https://salesforce.com/opportunity/001' },
        { name: 'WBD · Upfront Sponsorship Package', stage: 'Negotiation', priority: 'high', url: 'https://salesforce.com/opportunity/002' },
        { name: 'WBD · PMP Q3 Extension', stage: 'Discovery', priority: 'medium', url: null },
        { name: 'WBD · Ads Manager Pilot', stage: 'Qualification', priority: 'low', url: null },
      ],
      performance: {
        totalBooked: 8640000,
        annualGoal: 12000000,
        totalSpend: 7920000,
      },
      activationQoQ: {
        labels: ['Q1', 'Q2', 'Q3', 'Q4'],
        DIO:          [1200000, 980000,  0, 0],
        PMP:          [840000,  620000,  0, 0],
        Sponsorship:  [320000,  280000,  0, 0],
        ChannelSales: [180000,  240000,  0, 0],
        AdsManager:   [60000,   90000,   0, 0],
      },
      opportunities: {
        shortTerm: [
          { text: 'Pitch Q3 DIO renewal package before June 28 campaign end', done: false },
        ],
        longTerm: [
          { text: 'Develop Upfront 2026 proposal — focus on CTV reach + measurement story', done: false },
        ],
        challenges: [
          { text: 'Internal budget reallocation to digital display reducing CTV commitment', done: false },
        ],
      },
      contacts: [
        { name: 'Sarah Mitchell', title: 'VP, Media Investments', initials: 'SM', linkedin: 'https://linkedin.com/in/sarahmitchell' },
        { name: 'Jason Park', title: 'Director, Programmatic Strategy', initials: 'JP', linkedin: null },
        { name: 'Tiffany Ross', title: 'Media Planner', initials: 'TR', linkedin: null },
      ],
      salesActivity: [
        { date: '2025-06-10', product: 'DIO', response: 'Positive — Sarah confirmed intent to renew, awaiting legal review' },
        { date: '2025-05-28', product: 'Sponsorship', response: 'Held follow-up call, shared Upfront packaging deck' },
        { date: '2025-05-12', product: 'PMP', response: 'Neutral — Jason requested updated CPM benchmarks vs. competing platforms' },
        { date: '2025-04-30', product: 'Ads Manager', response: 'Intro call — team is evaluating self-serve options, low urgency' },
        { date: '2025-04-15', product: 'DIO', response: 'QBR presentation delivered, strong engagement on Measurement suite' },
        { date: '2025-03-22', product: 'PMP', response: 'Q1 wrap — exceeded delivery, client very satisfied with brand safety scores' },
      ],
      notes: 'WBD is navigating internal restructuring following the Discovery merger integration. Media investment decisions are being centralized through NYC HQ. Key relationship is with Sarah Mitchell — maintain monthly executive touchpoints. Their Upfront commitment is contingent on Measurement reporting improvements being delivered by Q3.',
      competitors: [
        {
          brand: 'YouTube TV',
          competitor: 'Google',
          ctvInvestment: '$12M+',
          buyingApproach: 'Programmatic-first via DV360; heavy YouTube Connected TV placements',
          targeting: ['Household income $100K+', 'Sports & entertainment enthusiasts', 'Cord-cutters 25–54'],
          creative: ['15s & 30s skippable pre-roll', 'Masthead takeovers for tent-pole events', 'Non-skippable bumper ads'],
          measurement: ['Google Ads reach & frequency', 'Brand Lift studies via Google Surveys', 'Attribution via Floodlight'],
        },
        {
          brand: 'Hulu',
          competitor: 'Disney',
          ctvInvestment: '$8.5M',
          buyingApproach: 'Direct IO with Disney Advertising, premium audience packages',
          targeting: ['18–49 general', 'Streaming-first households', 'High-income binge viewers'],
          creative: ['Branded entertainment integrations', 'Pause ads', 'Gateway ads (full-screen interstitial)'],
          measurement: ['Hulu Audience Data Platform', 'Nielsen DAR / OCR', 'Disney Audience Graph'],
        },
        {
          brand: 'Peacock',
          competitor: 'NBCUniversal',
          ctvInvestment: '$4.2M',
          buyingApproach: 'Mix of DIO and One Platform PMP',
          targeting: ['NBC broadcast loyalists', 'Sports fans (NFL/Olympics)', '35–64 demos'],
          creative: ['Ad-supported tier standard :30s', 'NBCU first-party segments activation', 'Sponsorship packages tied to live events'],
          measurement: ['One Platform audience verification', 'NBCUniversal Cross-Screen Attribution', 'Third-party: IAS, DoubleVerify'],
        },
      ],
    },
    netflix: {
      name: 'Netflix Advertising',
      short: 'NFLX',
      vertical: 'Technology',
      subVertical: 'Streaming / Ad-Supported',
      reminder: 'Upfront proposal due July 1',
      tags: ['Performance', 'AVOD Growth', 'Q3 Priority'],
      primaryKpiLabel: 'H1 Revenue',
      primaryKpiValue: '$2.1M · 64% to Goal',
      pacing: { quarterLabel: 'Q2 2025', quarterBooked: 1050000, quarterGoal: 1600000, pctToGoal: 66, revenueAtRisk: 210000, note: 'Netflix ad tier growth slower than projected. Revisit CPM conversation.' },
      sfOpps: [
        { name: 'Netflix · CTV DIO Package', stage: 'Discovery', priority: 'high', url: null },
      ],
      performance: { totalBooked: 2100000, annualGoal: 4800000, totalSpend: 1900000 },
      activationQoQ: { labels: ['Q1','Q2','Q3','Q4'], DIO:[600000,450000,0,0], PMP:[320000,280000,0,0], Sponsorship:[80000,60000,0,0], ChannelSales:[40000,50000,0,0], AdsManager:[20000,30000,0,0] },
      opportunities: { shortTerm:[{text:'Secure DIO deal before Q3 planning cycle',done:false}], longTerm:[{text:'Build Upfront 2026 case around measurement',done:false}], challenges:[{text:'Netflix ad inventory still maturing — limited targeting options',done:false}] },
      contacts: [{ name: 'Meredith Chen', title: 'Media Director', initials: 'MC', linkedin: null }],
      salesActivity: [
        { date: '2025-06-05', product: 'DIO', response: 'Intro meeting, strong interest in brand safety features' },
        { date: '2025-05-20', product: 'PMP', response: 'Shared PMP overview, requested CPM comparison vs. YouTube' },
      ],
      notes: 'Netflix is expanding their ad-supported tier rapidly. Early mover opportunity to lock in preferred placement.',
      competitors: [],
    },
    amazon: {
      name: 'Amazon Ads',
      short: 'AMZ',
      vertical: 'Retail / E-Commerce',
      subVertical: 'Performance + CTV',
      reminder: 'Q3 budget finalization call — June 25',
      tags: ['Performance', 'Retail Media', 'DIO Target'],
      primaryKpiLabel: 'Annual Pacing',
      primaryKpiValue: '$5.8M · 58% to Goal',
      pacing: { quarterLabel: 'Q2 2025', quarterBooked: 1640000, quarterGoal: 2500000, pctToGoal: 66, revenueAtRisk: 600000, note: 'Amazon shifting budget to Prime Video Ads. Opportunity to position Roku as complementary reach extension.' },
      sfOpps: [
        { name: 'Amazon · Fire TV Competitive Conquest', stage: 'Proposal Sent', priority: 'high', url: null },
        { name: 'Amazon · Q3 Sponsored Content', stage: 'Negotiation', priority: 'medium', url: null },
      ],
      performance: { totalBooked: 5800000, annualGoal: 10000000, totalSpend: 5200000 },
      activationQoQ: { labels:['Q1','Q2','Q3','Q4'], DIO:[1800000,840000,0,0], PMP:[920000,560000,0,0], Sponsorship:[160000,120000,0,0], ChannelSales:[80000,60000,0,0], AdsManager:[40000,40000,0,0] },
      opportunities: { shortTerm:[{text:'Position Roku as reach complement to Prime Video Ads',done:false}], longTerm:[{text:'Annual programmatic partnership agreement',done:false}], challenges:[{text:'Amazon building internal CTV inventory via Prime Video — direct competition',done:false}] },
      contacts: [
        { name: 'Derek Huang', title: 'Global Media Lead', initials: 'DH', linkedin: 'https://linkedin.com/in/derekhuang' },
        { name: 'Ashley Warren', title: 'Programmatic Manager', initials: 'AW', linkedin: null },
      ],
      salesActivity: [
        { date: '2025-06-08', product: 'DIO', response: 'Budget discussion — they are evaluating Prime Video vs. Roku incremental reach' },
        { date: '2025-05-30', product: 'PMP', response: 'Positive feedback on brand safety and measurement reporting' },
        { date: '2025-05-10', product: 'Sponsorship', response: 'Held sponsorship overview call, interest in Q4 tentpole packages' },
        { date: '2025-04-22', product: 'DIO', response: 'Q1 wrap — strong delivery, 102% pacing, client very happy' },
      ],
      notes: 'Amazon is one of the largest CTV advertisers. The Prime Video expansion is a risk, but also positions Amazon as a motivated buyer of incremental reach on Roku.',
      competitors: [],
    },
  },

  // Overview portfolio data
  portfolio: {
    totalRevenue: 42600000,
    sipGoal: 52000000,
    pctToSip: 82,
    loadedRevenue: 38900000,
    activeCampaignRevenue: 24100000,
    activationBreakdown: {
      DIO: { revenue: 18200000, pct: 43 },
      PMP: { revenue: 12400000, pct: 29 },
      Sponsorship: { revenue: 5800000, pct: 14 },
      ChannelSales: { revenue: 4200000, pct: 10 },
      AdsManager: { revenue: 2000000, pct: 5 },
    },
    dealTypePacing: [
      { type: '1:Many Advertiser', booked: 14200000, goal: 18000000, pct: 79 },
      { type: '1:Many Agency', booked: 16800000, goal: 20000000, pct: 84 },
      { type: '1:Many Hold Co (AHC)', booked: 8400000, goal: 10000000, pct: 84 },
      { type: 'Channel Sales', booked: 3200000, goal: 4000000, pct: 80 },
    ],
    revByDSP: [
      { dsp: 'The Trade Desk', revenue: 5200000, pct: 42 },
      { dsp: 'DV360 (Google)', revenue: 3100000, pct: 25 },
      { dsp: 'Amazon DSP', revenue: 2100000, pct: 17 },
      { dsp: 'Xandr (Microsoft)', revenue: 1000000, pct: 8 },
      { dsp: 'Other DSPs', revenue: 1000000, pct: 8 },
    ],
  },
};

// Colors for activation types
const ACT_COLORS = {
  DIO: '#6B2D8B',
  PMP: '#9B4DBB',
  Sponsorship: '#C07FDE',
  ChannelSales: '#4A90D9',
  AdsManager: '#78C1F0',
};

// ── HELPERS ───────────────────────────────────────────────────
const $ = (sel, ctx = document) => ctx.querySelector(sel);
const $$ = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];
const fmt = (n) => n >= 1e6 ? `$${(n/1e6).toFixed(1)}M` : n >= 1e3 ? `$${(n/1e3).toFixed(0)}K` : `$${n}`;
const fmtPct = (n) => `${n}%`;
const esc = (s) => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');

function pillClass(priority) {
  if (priority === 'high') return 'red';
  if (priority === 'medium') return 'amber';
  return 'gray';
}

function stageClass(stage) {
  const s = stage.toLowerCase();
  if (s.includes('negotiation') || s.includes('close')) return 'purple';
  if (s.includes('proposal')) return 'blue';
  if (s.includes('qualification') || s.includes('discovery')) return 'amber';
  return 'gray';
}

// ── TAB SWITCHING ─────────────────────────────────────────────
function switchTab(tabId) {
  state.activeTab = tabId;
  $$('.tab-btn').forEach(b => b.classList.toggle('active', b.dataset.tab === tabId));
  $$('.tab-panel').forEach(p => p.classList.toggle('active', p.id === `panel-${tabId}`));
  if (tabId === 'account-plan') renderAccountPlan();
  if (tabId === 'data-input') renderDataInput();
}

// ── ACCOUNT SWITCHING ─────────────────────────────────────────
function selectAccount(id) {
  state.activeAccount = id;
  $$('.account-item').forEach(el => el.classList.toggle('active', el.dataset.account === id));

  if (id === 'all') {
    $$('.tab-panel').forEach(p => p.classList.toggle('active', p.id === 'panel-overview'));
    $('#main-tabs-nav').style.display = 'none';
    renderOverview();
  } else {
    $('#main-tabs-nav').style.display = '';
    switchTab(state.activeTab === 'data-input' ? 'data-input' : 'account-plan');
  }
}

function accountSearch(query) {
  const q = query.toLowerCase().trim();
  $$('.account-item:not(.all-accounts)').forEach(el => {
    const name = el.dataset.name || '';
    el.style.display = (!q || name.toLowerCase().includes(q)) ? '' : 'none';
  });
}

// ── OVERVIEW RENDER ───────────────────────────────────────────
function renderOverview() {
  const p = state.portfolio;

  // KPI cards
  const kpiCards = [
    { label: 'Total Revenue', value: fmt(p.totalRevenue), sub: 'YTD through Q2', bar: null },
    { label: 'SIP Goal', value: fmt(p.sipGoal), sub: 'Annual target', bar: null },
    { label: '% to SIP Goal', value: fmtPct(p.pctToSip), sub: 'Ahead of linear pace', bar: { pct: p.pctToSip, color: p.pctToSip >= 80 ? 'green' : p.pctToSip >= 60 ? 'amber' : 'red' } },
    { label: 'Total Loaded Revenue', value: fmt(p.loadedRevenue), sub: 'In platform', bar: null },
    { label: 'Active Campaign Rev', value: fmt(p.activeCampaignRevenue), sub: 'Currently live', bar: null },
  ];

  $('#overview-kpi-grid').innerHTML = kpiCards.map(k => `
    <div class="kpi-card">
      <div class="kpi-label">${k.label}</div>
      <div class="kpi-value">${k.value}</div>
      <div class="kpi-sub">${k.sub}</div>
      ${k.bar ? `<div class="kpi-bar"><div class="progress-track"><div class="progress-fill ${k.bar.color}" style="width:${k.bar.pct}%"></div></div></div>` : ''}
    </div>
  `).join('');

  // Activation breakdown
  const actKeys = Object.keys(p.activationBreakdown);
  $('#overview-activation-grid').innerHTML = actKeys.map(k => {
    const a = p.activationBreakdown[k];
    return `
      <div class="activation-card">
        <div class="act-label">${k === 'PMP' ? 'Programmatic (PMP/PG)' : k === 'ChannelSales' ? 'Channel Sales' : k === 'AdsManager' ? 'Ads Manager' : k}</div>
        <div class="act-value">${fmt(a.revenue)}</div>
        <div class="act-sub">${a.pct}% of total</div>
        <div style="margin-top:8px"><div class="progress-track"><div class="progress-fill purple" style="width:${a.pct}%"></div></div></div>
      </div>
    `;
  }).join('');

  // Deal type pacing table
  $('#overview-deal-table').innerHTML = `
    <table class="deal-table">
      <thead><tr>
        <th>Deal Type</th><th>Booked</th><th>Goal</th><th>% to Goal</th><th>Pacing</th>
      </tr></thead>
      <tbody>
        ${p.dealTypePacing.map(d => `
          <tr>
            <td style="font-weight:600">${d.type}</td>
            <td>${fmt(d.booked)}</td>
            <td>${fmt(d.goal)}</td>
            <td><span class="pill ${d.pct>=80?'green':d.pct>=60?'amber':'red'}">${d.pct}%</span></td>
            <td style="min-width:120px">
              <div class="progress-track"><div class="progress-fill ${d.pct>=80?'green':d.pct>=60?'amber':'red'}" style="width:${d.pct}%"></div></div>
            </td>
          </tr>
        `).join('')}
      </tbody>
    </table>
  `;

  // DSP table
  $('#overview-dsp-table').innerHTML = `
    <table class="deal-table">
      <thead><tr><th>DSP</th><th>Revenue</th><th>Share</th></tr></thead>
      <tbody>
        ${p.revByDSP.map(d => `
          <tr>
            <td style="font-weight:600">${d.dsp}</td>
            <td>${fmt(d.revenue)}</td>
            <td>
              <div style="display:flex;align-items:center;gap:8px">
                <div class="progress-track" style="width:80px"><div class="progress-fill purple" style="width:${d.pct}%"></div></div>
                <span style="font-size:11px;color:var(--text-muted)">${d.pct}%</span>
              </div>
            </td>
          </tr>
        `).join('')}
      </tbody>
    </table>
  `;

  // Stacked bar chart for health
  renderStackedBar('overview-health-chart', buildPortfolioChartData());
}

function buildPortfolioChartData() {
  // aggregate all accounts Q1/Q2
  const labels = ['Q1','Q2'];
  const sets = { DIO:[0,0], PMP:[0,0], Sponsorship:[0,0], ChannelSales:[0,0], AdsManager:[0,0] };
  Object.values(state.accounts).forEach(acct => {
    const aq = acct.activationQoQ;
    ['DIO','PMP','Sponsorship','ChannelSales','AdsManager'].forEach(k => {
      sets[k][0] += aq[k][0] || 0;
      sets[k][1] += aq[k][1] || 0;
    });
  });
  return { labels, sets };
}

function renderStackedBar(containerId, data) {
  const el = $(`#${containerId}`);
  if (!el) return;
  const maxVal = data.labels.map((_, i) =>
    Object.values(data.sets).reduce((s, v) => s + (v[i]||0), 0)
  ).reduce((a, b) => Math.max(a, b), 1);

  const keys = Object.keys(data.sets);
  const bars = data.labels.map((label, qi) => {
    const total = keys.reduce((s, k) => s + (data.sets[k][qi]||0), 0);
    const pct = total / maxVal * 100;
    const segments = keys.map(k => {
      const h = ((data.sets[k][qi]||0) / maxVal * 100);
      if (h <= 0) return '';
      const color = ACT_COLORS[k] || '#ccc';
      return `<div class="bar-segment" style="height:${h}%;background:${color}" title="${k}: ${fmt(data.sets[k][qi]||0)}"></div>`;
    }).join('');
    return `
      <div class="chart-bar-group">
        <div class="chart-bar-stack" style="height:140px">${segments}</div>
        <div class="chart-qlabel">${label}</div>
        <div style="font-size:10px;color:var(--text-muted)">${fmt(total)}</div>
      </div>
    `;
  }).join('');

  const legend = keys.map(k => `
    <div class="legend-item">
      <div class="legend-dot" style="background:${ACT_COLORS[k]}"></div>
      <span>${k === 'ChannelSales' ? 'Channel Sales' : k === 'AdsManager' ? 'Ads Manager' : k === 'PMP' ? 'PMP/PG' : k}</span>
    </div>
  `).join('');

  el.innerHTML = `
    <div style="display:flex;gap:12px;align-items:flex-end;width:100%;margin-bottom:8px">${bars}</div>
    <div class="chart-legend">${legend}</div>
  `;
}

// ── ACCOUNT PLAN RENDER ───────────────────────────────────────
function renderAccountPlan() {
  const acct = state.accounts[state.activeAccount];
  if (!acct) return;
  const year = state.currentYear;

  // Header
  $('#ap-account-name').textContent = acct.name;
  $('#ap-account-sub').textContent = `Roku Intelligence Center · FY ${year}`;
  $('#ap-year-display').textContent = year;
  $('#ap-reminder-text').textContent = acct.reminder;

  // Summary bar
  $('#ap-summary-kpi-label').textContent = acct.primaryKpiLabel;
  $('#ap-summary-kpi-value').textContent = acct.primaryKpiValue;
  $('#ap-summary-account').textContent = acct.name;
  $('#ap-summary-vertical').textContent = acct.vertical;
  $('#ap-summary-subvertical').textContent = acct.subVertical;
  $('#ap-summary-tags').innerHTML = acct.tags.map(t => `<span class="summary-tag">${esc(t)}</span>`).join('');

  // Pacing
  const pac = acct.pacing;
  $('#ap-pacing-quarter').textContent = pac.quarterLabel;
  $('#ap-pacing-booked').textContent = fmt(pac.quarterBooked);
  $('#ap-pacing-goal').textContent = fmt(pac.quarterGoal);
  $('#ap-pacing-pct').textContent = fmtPct(pac.pctToGoal);
  $('#ap-pacing-risk').textContent = fmt(pac.revenueAtRisk);
  $('#ap-pacing-bar').style.width = `${pac.pctToGoal}%`;
  $('#ap-pacing-bar').className = `progress-fill ${pac.pctToGoal >= 80 ? 'green' : pac.pctToGoal >= 60 ? 'amber' : 'red'}`;
  $('#ap-pacing-note').textContent = pac.note;

  // SF Opps
  $('#ap-sf-opps').innerHTML = acct.sfOpps.map(o => `
    <div class="sf-opp-item">
      <div>
        <div class="sf-opp-name">
          ${o.url ? `<a href="${esc(o.url)}" target="_blank" rel="noopener">${esc(o.name)}</a>` : esc(o.name)}
        </div>
        <div class="sf-opp-meta">${esc(o.stage)}</div>
      </div>
      <div class="sf-opp-right">
        <span class="pill ${stageClass(o.stage)}">${esc(o.stage)}</span>
        ${o.priority ? `<span class="pill ${pillClass(o.priority)}">${o.priority}</span>` : ''}
      </div>
    </div>
  `).join('');

  // Performance
  const perf = acct.performance;
  $('#ap-perf-booked').textContent = fmt(perf.totalBooked);
  $('#ap-perf-goal').textContent = fmt(perf.annualGoal);
  $('#ap-perf-spend').textContent = fmt(perf.totalSpend);
  const annualPct = Math.round(perf.totalBooked / perf.annualGoal * 100);
  $('#ap-perf-pct').textContent = `${annualPct}%`;
  $('#ap-annual-pct-bar').style.width = `${annualPct}%`;
  $('#ap-annual-pct-bar').className = `progress-fill ${annualPct >= 80 ? 'green' : annualPct >= 60 ? 'amber' : 'red'}`;

  // QoQ chart
  renderStackedBar('ap-qoq-chart', {
    labels: acct.activationQoQ.labels,
    sets: {
      DIO: acct.activationQoQ.DIO,
      PMP: acct.activationQoQ.PMP,
      Sponsorship: acct.activationQoQ.Sponsorship,
      ChannelSales: acct.activationQoQ.ChannelSales,
      AdsManager: acct.activationQoQ.AdsManager,
    }
  });

  // Opportunities
  renderOpportunities(acct);

  // Contacts
  renderContacts(acct);

  // Sales activity
  renderSalesActivity(acct, false);

  // Notes
  $('#ap-notes').value = acct.notes || '';

  // Competitors
  renderCompetitors(acct);
}

function renderOpportunities(acct) {
  const opp = acct.opportunities;

  function oppList(items, key, sectionEl) {
    sectionEl.innerHTML = items.map((item, i) => `
      <div class="opp-item ${item.done ? 'done' : ''}" data-key="${key}" data-idx="${i}">
        <input type="checkbox" ${item.done ? 'checked' : ''} onchange="toggleOpp('${key}',${i})">
        <span>${esc(item.text)}</span>
      </div>
    `).join('');
  }

  oppList(opp.shortTerm, 'shortTerm', $('#ap-short-term-list'));
  oppList(opp.longTerm, 'longTerm', $('#ap-long-term-list'));
  oppList(opp.challenges, 'challenges', $('#ap-challenges-list'));
}

function toggleOpp(key, idx) {
  const acct = state.accounts[state.activeAccount];
  acct.opportunities[key][idx].done = !acct.opportunities[key][idx].done;
  renderOpportunities(acct);
}

function addOppItem(key) {
  const text = prompt('Enter new item:');
  if (!text) return;
  state.accounts[state.activeAccount].opportunities[key].push({ text, done: false });
  renderOpportunities(state.accounts[state.activeAccount]);
}

function renderContacts(acct) {
  $('#ap-contacts-list').innerHTML = acct.contacts.map(c => `
    <div class="contact-item">
      <div class="contact-avatar">${esc(c.initials)}</div>
      <div class="contact-info">
        <div class="contact-name">
          ${c.linkedin ? `<a href="${esc(c.linkedin)}" target="_blank" rel="noopener">${esc(c.name)}</a>` : esc(c.name)}
          ${c.linkedin ? `<a href="${esc(c.linkedin)}" target="_blank" rel="noopener" style="margin-left:5px;color:var(--text-muted);font-size:10px">↗ LinkedIn</a>` : ''}
        </div>
        <div class="contact-title">${esc(c.title)}</div>
      </div>
    </div>
  `).join('');
}

function renderSalesActivity(acct, expanded) {
  const activities = expanded ? acct.salesActivity : acct.salesActivity.slice(0, 4);
  const products = [...new Set(acct.salesActivity.map(a => a.product))];
  const filterSel = $('#ap-activity-filter');
  if (filterSel) {
    const current = filterSel.value;
    filterSel.innerHTML = `<option value="">All Products</option>` +
      products.map(p => `<option value="${esc(p)}" ${current===p?'selected':''}>${esc(p)}</option>`).join('');
  }
  const filter = filterSel ? filterSel.value : '';
  const filtered = activities.filter(a => !filter || a.product === filter);
  $('#ap-activity-body').innerHTML = filtered.map(a => `
    <tr>
      <td style="white-space:nowrap;color:var(--text-muted)">${a.date}</td>
      <td><span class="pill purple">${esc(a.product)}</span></td>
      <td>${esc(a.response)}</td>
    </tr>
  `).join('');
  const expandBtn = $('#ap-expand-btn');
  if (expandBtn) {
    expandBtn.textContent = expanded ? 'Show Less' : `Show All (${acct.salesActivity.length})`;
    expandBtn.onclick = () => renderSalesActivity(acct, !expanded);
  }
}

function renderCompetitors(acct) {
  const container = $('#ap-competitors-container');
  if (!acct.competitors || acct.competitors.length === 0) {
    container.innerHTML = `<div style="color:var(--text-muted);font-size:12px;padding:16px 0">No competitor data yet. Enter competitor brands above and click Generate.</div>`;
    return;
  }
  container.innerHTML = `<div class="competitors-grid">` +
    acct.competitors.map(c => `
      <div class="competitor-card">
        <div class="competitor-card-header">
          <div class="comp-name">${esc(c.competitor)}</div>
          <div class="comp-brand">${esc(c.brand)}</div>
        </div>
        <div class="competitor-card-body">
          <div class="comp-row"><div class="comp-row-label">CTV Investment</div><div class="comp-row-value">${esc(c.ctvInvestment)}</div></div>
          <div class="comp-row"><div class="comp-row-label">Buying Approach</div><div class="comp-row-value">${esc(c.buyingApproach)}</div></div>
          <div class="comp-row"><div class="comp-row-label">Targeting</div><div class="comp-row-value"><ul>${c.targeting.map(t=>`<li>${esc(t)}</li>`).join('')}</ul></div></div>
          <div class="comp-row"><div class="comp-row-label">Creative</div><div class="comp-row-value"><ul>${c.creative.map(t=>`<li>${esc(t)}</li>`).join('')}</ul></div></div>
          <div class="comp-row"><div class="comp-row-label">Measurement</div><div class="comp-row-value"><ul>${c.measurement.map(t=>`<li>${esc(t)}</li>`).join('')}</ul></div></div>
        </div>
      </div>
    `).join('') + `</div>`;
}

// ── COMPETITOR GENERATION (AI Hub hook) ───────────────────────
async function generateCompetitors() {
  const inputs = $$('.competitor-brand-input').map(el => el.value.trim()).filter(Boolean);
  if (inputs.length === 0) {
    alert('Enter at least one competitor brand name.');
    return;
  }

  const btn = $('#btn-generate-competitors');
  const container = $('#ap-competitors-container');
  btn.disabled = true;
  btn.textContent = 'Generating…';
  container.innerHTML = `<div class="loading-state"><div class="spinner"></div><span>Fetching competitor intelligence from Roku AI Hub…</span></div>`;

  try {
    // This is the Roku AI Hub hook — wire to live API here
    // Example prompt structure for the API:
    const prompt = `You are a CTV media intelligence analyst. For each competitor brand listed, provide structured intelligence in JSON format. Brands: ${inputs.join(', ')}.
Return an array of objects with fields:
- brand (string): the brand name
- competitor (string): parent company or platform
- ctvInvestment (string): estimated CTV ad investment
- buyingApproach (string): description of buying strategy
- targeting (array of strings): 3 targeting bullet points
- creative (array of strings): 3 creative format bullet points
- measurement (array of strings): 3 measurement/attribution approaches
Only return valid JSON array. No commentary.`;

    // Simulated response for demo — replace with actual AI Hub fetch
    await new Promise(r => setTimeout(r, 1600));
    const generated = inputs.map(brand => ({
      brand,
      competitor: brand,
      ctvInvestment: 'Intelligence pending',
      buyingApproach: `${brand} is investing in CTV programmatically, leveraging first-party data for audience targeting across connected TV environments.`,
      targeting: ['Behavioral & interest-based targeting', 'First-party CRM audience extension', 'Lookalike modeling against high-LTV customers'],
      creative: ['15s & 30s video units', 'Interactive overlay ads', 'Branded content integrations'],
      measurement: ['Multi-touch attribution', 'Brand lift surveys', 'View-through conversion tracking'],
    }));

    state.accounts[state.activeAccount].competitors = generated;
    renderCompetitors(state.accounts[state.activeAccount]);

    // Sync competitor input on data tab
    syncCompetitorInputs();

  } catch (e) {
    container.innerHTML = `<div style="color:var(--accent-red);font-size:12px;padding:16px 0">Generation failed. Check Roku AI Hub connection.</div>`;
  } finally {
    btn.disabled = false;
    btn.textContent = 'Generate Intelligence';
  }
}

function syncCompetitorInputs() {
  const acct = state.accounts[state.activeAccount];
  $$('.competitor-brand-input').forEach((el, i) => {
    if (acct.competitors && acct.competitors[i]) el.value = acct.competitors[i].brand;
  });
}

// ── DATA INPUT RENDER ─────────────────────────────────────────
function renderDataInput() {
  const acct = state.accounts[state.activeAccount];
  if (!acct) return;

  // Header fields
  $('#di-account-name').value = acct.name;
  $('#di-year').value = state.currentYear;
  $('#di-vertical').value = acct.vertical;
  $('#di-subvertical').value = acct.subVertical;
  $('#di-reminder').value = acct.reminder;
  $('#di-tags').value = acct.tags.join(', ');
  $('#di-kpi-label').value = acct.primaryKpiLabel;
  $('#di-kpi-value').value = acct.primaryKpiValue;

  // Pacing
  const pac = acct.pacing;
  $('#di-pac-quarter').value = pac.quarterLabel;
  $('#di-pac-booked').value = pac.quarterBooked;
  $('#di-pac-goal').value = pac.quarterGoal;
  $('#di-pac-pct').value = pac.pctToGoal;
  $('#di-pac-risk').value = pac.revenueAtRisk;
  $('#di-pac-note').value = pac.note;

  // Perf
  $('#di-perf-booked').value = acct.performance.totalBooked;
  $('#di-perf-goal').value = acct.performance.annualGoal;
  $('#di-perf-spend').value = acct.performance.totalSpend;

  // Notes
  $('#di-notes').value = acct.notes || '';

  // SF Opps table
  renderDiSfOpps(acct);

  // Activation table
  renderDiActivation(acct);

  // Contacts
  renderDiContacts(acct);

  // Activities
  renderDiActivities(acct);

  // Opportunities
  renderDiOpportunities(acct);

  // Competitor inputs
  const compInputs = $$('.di-competitor-input');
  compInputs.forEach((el, i) => {
    if (acct.competitors && acct.competitors[i]) el.value = acct.competitors[i].brand;
    else el.value = '';
  });
}

function renderDiSfOpps(acct) {
  const tbody = $('#di-sf-opps-body');
  if (!tbody) return;
  tbody.innerHTML = acct.sfOpps.map((o, i) => `
    <tr>
      <td><input value="${esc(o.name)}" onchange="updateSfOpp(${i},'name',this.value)" placeholder="Opportunity name"></td>
      <td><input value="${esc(o.stage)}" onchange="updateSfOpp(${i},'stage',this.value)" placeholder="Stage"></td>
      <td><input value="${esc(o.url||'')}" onchange="updateSfOpp(${i},'url',this.value)" placeholder="https://..."></td>
      <td>
        <select onchange="updateSfOpp(${i},'priority',this.value)">
          <option value="high" ${o.priority==='high'?'selected':''}>High</option>
          <option value="medium" ${o.priority==='medium'?'selected':''}>Medium</option>
          <option value="low" ${o.priority==='low'?'selected':''}>Low</option>
        </select>
      </td>
      <td><button class="btn-delete-row" onclick="deleteSfOpp(${i})" title="Remove">×</button></td>
    </tr>
  `).join('');
}

function updateSfOpp(i, field, val) {
  state.accounts[state.activeAccount].sfOpps[i][field] = val || null;
}
function deleteSfOpp(i) {
  state.accounts[state.activeAccount].sfOpps.splice(i, 1);
  renderDiSfOpps(state.accounts[state.activeAccount]);
}
function addSfOpp() {
  state.accounts[state.activeAccount].sfOpps.push({ name: 'New Opportunity', stage: 'Qualification', priority: 'medium', url: null });
  renderDiSfOpps(state.accounts[state.activeAccount]);
}

function renderDiActivation(acct) {
  const tbody = $('#di-activation-body');
  if (!tbody) return;
  const aq = acct.activationQoQ;
  const quarters = ['Q1','Q2','Q3','Q4'];
  tbody.innerHTML = quarters.map((q, qi) => `
    <tr>
      <td style="font-weight:600;color:var(--text-secondary)">${q}</td>
      ${['DIO','PMP','Sponsorship','ChannelSales','AdsManager'].map(k => `
        <td><input type="number" value="${aq[k][qi]||0}" onchange="updateActivation('${k}',${qi},this.value)" style="width:90px"></td>
      `).join('')}
    </tr>
  `).join('');
}

function updateActivation(key, qi, val) {
  state.accounts[state.activeAccount].activationQoQ[key][qi] = parseFloat(val) || 0;
}

function renderDiContacts(acct) {
  const tbody = $('#di-contacts-body');
  if (!tbody) return;
  tbody.innerHTML = acct.contacts.map((c, i) => `
    <tr>
      <td><input value="${esc(c.name)}" onchange="updateContact(${i},'name',this.value)"></td>
      <td><input value="${esc(c.title)}" onchange="updateContact(${i},'title',this.value)"></td>
      <td><input value="${esc(c.initials)}" onchange="updateContact(${i},'initials',this.value)" style="width:60px"></td>
      <td><input value="${esc(c.linkedin||'')}" onchange="updateContact(${i},'linkedin',this.value)" placeholder="LinkedIn URL"></td>
      <td><button class="btn-delete-row" onclick="deleteContact(${i})">×</button></td>
    </tr>
  `).join('');
}

function updateContact(i, field, val) { state.accounts[state.activeAccount].contacts[i][field] = val || null; }
function deleteContact(i) { state.accounts[state.activeAccount].contacts.splice(i, 1); renderDiContacts(state.accounts[state.activeAccount]); }
function addContact() {
  state.accounts[state.activeAccount].contacts.push({ name: 'New Contact', title: '', initials: '?', linkedin: null });
  renderDiContacts(state.accounts[state.activeAccount]);
}

function renderDiActivities(acct) {
  const tbody = $('#di-activities-body');
  if (!tbody) return;
  tbody.innerHTML = acct.salesActivity.map((a, i) => `
    <tr>
      <td><input type="date" value="${esc(a.date)}" onchange="updateActivity(${i},'date',this.value)"></td>
      <td><input value="${esc(a.product)}" onchange="updateActivity(${i},'product',this.value)" style="width:100px"></td>
      <td><input value="${esc(a.response)}" onchange="updateActivity(${i},'response',this.value)"></td>
      <td><button class="btn-delete-row" onclick="deleteActivity(${i})">×</button></td>
    </tr>
  `).join('');
}

function updateActivity(i, field, val) { state.accounts[state.activeAccount].salesActivity[i][field] = val; }
function deleteActivity(i) { state.accounts[state.activeAccount].salesActivity.splice(i, 1); renderDiActivities(state.accounts[state.activeAccount]); }
function addActivity() {
  state.accounts[state.activeAccount].salesActivity.unshift({ date: new Date().toISOString().split('T')[0], product: '', response: '' });
  renderDiActivities(state.accounts[state.activeAccount]);
}

function renderDiOpportunities(acct) {
  const opp = acct.opportunities;
  ['shortTerm','longTerm','challenges'].forEach(key => {
    const el = $(`#di-${key}-list`);
    if (!el) return;
    el.innerHTML = opp[key].map((item, i) => `
      <tr>
        <td>
          <input value="${esc(item.text)}" onchange="updateOppText('${key}',${i},this.value)" style="width:100%">
        </td>
        <td>
          <label style="display:flex;align-items:center;gap:5px;font-size:11px;color:var(--text-secondary)">
            <input type="checkbox" ${item.done?'checked':''} onchange="toggleOppDi('${key}',${i})"> Done
          </label>
        </td>
        <td><button class="btn-delete-row" onclick="deleteOppItem('${key}',${i})">×</button></td>
      </tr>
    `).join('');
  });
}

function updateOppText(key, i, val) { state.accounts[state.activeAccount].opportunities[key][i].text = val; }
function toggleOppDi(key, i) { state.accounts[state.activeAccount].opportunities[key][i].done = !state.accounts[state.activeAccount].opportunities[key][i].done; }
function deleteOppItem(key, i) {
  state.accounts[state.activeAccount].opportunities[key].splice(i, 1);
  renderDiOpportunities(state.accounts[state.activeAccount]);
}
function addOppDi(key) {
  state.accounts[state.activeAccount].opportunities[key].push({ text: '', done: false });
  renderDiOpportunities(state.accounts[state.activeAccount]);
}

// ── SAVE DATA INPUT ───────────────────────────────────────────
function saveDataInput() {
  const acct = state.accounts[state.activeAccount];

  acct.name = $('#di-account-name').value;
  state.currentYear = parseInt($('#di-year').value) || state.currentYear;
  acct.vertical = $('#di-vertical').value;
  acct.subVertical = $('#di-subvertical').value;
  acct.reminder = $('#di-reminder').value;
  acct.tags = $('#di-tags').value.split(',').map(t => t.trim()).filter(Boolean);
  acct.primaryKpiLabel = $('#di-kpi-label').value;
  acct.primaryKpiValue = $('#di-kpi-value').value;
  acct.pacing.quarterLabel = $('#di-pac-quarter').value;
  acct.pacing.quarterBooked = parseFloat($('#di-pac-booked').value) || 0;
  acct.pacing.quarterGoal = parseFloat($('#di-pac-goal').value) || 0;
  acct.pacing.pctToGoal = parseFloat($('#di-pac-pct').value) || 0;
  acct.pacing.revenueAtRisk = parseFloat($('#di-pac-risk').value) || 0;
  acct.pacing.note = $('#di-pac-note').value;
  acct.performance.totalBooked = parseFloat($('#di-perf-booked').value) || 0;
  acct.performance.annualGoal = parseFloat($('#di-perf-goal').value) || 0;
  acct.performance.totalSpend = parseFloat($('#di-perf-spend').value) || 0;
  acct.notes = $('#di-notes').value;

  // Update sidebar account name
  const sideEl = $(`.account-item[data-account="${state.activeAccount}"] .account-item-name`);
  if (sideEl) sideEl.textContent = acct.name;

  const statusEl = $('#di-save-status');
  if (statusEl) {
    statusEl.textContent = `Saved at ${new Date().toLocaleTimeString()}`;
    setTimeout(() => { statusEl.textContent = ''; }, 3000);
  }

  if (state.activeTab === 'account-plan') renderAccountPlan();
}

// ── CSV UPLOAD ─────────────────────────────────────────────────
function handleCsvUpload(file) {
  if (!file) return;
  const reader = new FileReader();
  reader.onload = (e) => {
    try {
      const lines = e.target.result.trim().split('\n');
      const headers = lines[0].split(',').map(h => h.trim());
      const acct = state.accounts[state.activeAccount];
      const keyMap = {
        'Direct IO (DIO)': 'DIO',
        'Programmatic (PMP / PG)': 'PMP',
        'Sponsorship': 'Sponsorship',
        'Channel Sales': 'ChannelSales',
        'Ads Manager': 'AdsManager',
      };
      for (let li = 1; li < lines.length; li++) {
        const vals = lines[li].split(',').map(v => v.trim());
        const q = vals[0];
        const qi = ['Q1','Q2','Q3','Q4'].indexOf(q);
        if (qi < 0) continue;
        headers.forEach((h, hi) => {
          const k = keyMap[h];
          if (k && vals[hi] !== undefined) acct.activationQoQ[k][qi] = parseFloat(vals[hi]) || 0;
        });
      }
      renderDiActivation(acct);
      alert('CSV imported successfully.');
    } catch (err) {
      alert('CSV parse error. Please check the format.');
    }
  };
  reader.readAsText(file);
}

// ── YEAR SWITCHER ─────────────────────────────────────────────
function changeYear(delta) {
  state.currentYear += delta;
  renderAccountPlan();
}

// ── NEW ACCOUNT ───────────────────────────────────────────────
function createNewAccount() {
  const name = prompt('Account name:');
  if (!name) return;
  const id = name.toLowerCase().replace(/\s+/g, '_').replace(/[^a-z0-9_]/g, '');
  const initials = name.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2);
  state.accounts[id] = {
    name,
    short: initials,
    vertical: 'Unknown',
    subVertical: '',
    reminder: '',
    tags: [],
    primaryKpiLabel: 'Annual Goal',
    primaryKpiValue: 'Not set',
    pacing: { quarterLabel: 'Q1 2025', quarterBooked: 0, quarterGoal: 0, pctToGoal: 0, revenueAtRisk: 0, note: '' },
    sfOpps: [],
    performance: { totalBooked: 0, annualGoal: 0, totalSpend: 0 },
    activationQoQ: { labels:['Q1','Q2','Q3','Q4'], DIO:[0,0,0,0], PMP:[0,0,0,0], Sponsorship:[0,0,0,0], ChannelSales:[0,0,0,0], AdsManager:[0,0,0,0] },
    opportunities: { shortTerm:[{text:'',done:false}], longTerm:[{text:'',done:false}], challenges:[{text:'',done:false}] },
    contacts: [{ name: 'New Contact', title: '', initials: initials, linkedin: null }],
    salesActivity: [],
    notes: '',
    competitors: [],
  };
  addAccountToSidebar(id, state.accounts[id]);
  selectAccount(id);
}

function addAccountToSidebar(id, acct) {
  const list = $('#account-list');
  const div = document.createElement('div');
  div.className = 'account-item';
  div.dataset.account = id;
  div.dataset.name = acct.name;
  div.onclick = () => selectAccount(id);
  div.innerHTML = `
    <div class="account-avatar">${esc(acct.short)}</div>
    <div class="account-item-info">
      <div class="account-item-name">${esc(acct.name)}</div>
      <div class="account-item-meta">${esc(acct.vertical)}</div>
    </div>
  `;
  list.appendChild(div);
}

// ── INIT ──────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  // Tab buttons
  $$('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => switchTab(btn.dataset.tab));
  });

  // Account sidebar clicks
  $$('.account-item').forEach(el => {
    el.addEventListener('click', () => selectAccount(el.dataset.account));
  });

  // Account search
  const searchInput = $('#account-search-input');
  if (searchInput) searchInput.addEventListener('input', e => accountSearch(e.target.value));

  // File upload zone
  const uploadZone = $('#csv-upload-zone');
  const fileInput = $('#csv-file-input');
  if (uploadZone && fileInput) {
    uploadZone.addEventListener('click', () => fileInput.click());
    uploadZone.addEventListener('dragover', e => { e.preventDefault(); uploadZone.classList.add('drag-over'); });
    uploadZone.addEventListener('dragleave', () => uploadZone.classList.remove('drag-over'));
    uploadZone.addEventListener('drop', e => {
      e.preventDefault();
      uploadZone.classList.remove('drag-over');
      handleCsvUpload(e.dataTransfer.files[0]);
    });
    fileInput.addEventListener('change', e => handleCsvUpload(e.target.files[0]));
  }

  // Render initial state — All Accounts portfolio view
  selectAccount('all');
});
