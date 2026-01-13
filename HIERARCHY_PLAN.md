# 🏢 Multi-Level Hierarchy System Plan

## Overview

Expanding the Sales Performance System to support organizational hierarchy with role-based dashboards.

---

## 🎯 Organizational Structure

```
Division Head (Executive Level)
    ├── Area Manager 1 (Regional Level)
    │   ├── Agent 1
    │   ├── Agent 2
    │   └── Agent 3
    ├── Area Manager 2
    │   ├── Agent 4
    │   ├── Agent 5
    │   └── Agent 6
    └── Area Manager 3
        ├── Agent 7
        ├── Agent 8
        └── Agent 9
```

---

## 👥 User Roles

### 1. Agent (Individual Contributor)
**Responsibilities:**
- Track own performance
- View personal goals
- See individual metrics

**Dashboard Access:**
- Own performance metrics
- Own sales data
- Personal targets
- Own activity history
- Personal AI predictions

### 2. Area Manager (Team Lead)
**Responsibilities:**
- Manage team of agents
- Monitor team performance
- Identify at-risk agents
- Coach and support team

**Dashboard Access:**
- All agents in their area
- Team performance summary
- Team comparisons
- Area-wide metrics
- Team rankings
- At-risk agent alerts

### 3. Division Head (Executive)
**Responsibilities:**
- Oversee multiple areas
- Monitor division performance
- Strategic decision making
- Resource allocation

**Dashboard Access:**
- All areas performance
- Division-wide metrics
- Area comparisons
- Top/bottom performers
- Division trends
- Executive summaries

---

## 📊 Dashboard Designs

### 1. Agent Dashboard

**Layout:**
```
┌─────────────────────────────────────────┐
│ My Performance                          │
├─────────────────────────────────────────┤
│ [Personal Stats Cards]                  │
│ - Current Month Progress                │
│ - Activities Count                      │
│ - Sales vs Target                       │
│ - Ranking in Area                       │
├─────────────────────────────────────────┤
│ [Progress Section]                      │
│ - Sales Progress Bar                    │
│ - Activity Metrics                      │
│ - Daily/Weekly Trends                   │
├─────────────────────────────────────────┤
│ [AI Insights]                           │
│ - Prediction: HIT/MISS                  │
│ - Confidence Score                      │
│ - Recommendations                       │
│ - Areas to Improve                      │
└─────────────────────────────────────────┘
```

**Features:**
- Personal goal tracking
- Daily activity log
- Performance trends
- Comparison with team average
- Actionable recommendations

---

### 2. Area Manager Dashboard

**Layout:**
```
┌─────────────────────────────────────────┐
│ My Team - [Area Name]                   │
├─────────────────────────────────────────┤
│ [Area Summary Cards]                    │
│ - Total Agents: 8                       │
│ - Team Target: $4.8M                    │
│ - Current Sales: $3.2M (67%)            │
│ - At Risk: 2 agents                     │
├─────────────────────────────────────────┤
│ [Risk Alerts]                           │
│ 🔴 High Risk (2)                        │
│ 🟡 Medium Risk (3)                      │
│ 🟢 Low Risk (3)                         │
├─────────────────────────────────────────┤
│ [Agent Cards - Sorted by Risk]          │
│ [Agent 1] HIGH RISK                     │
│ [Agent 2] HIGH RISK                     │
│ [Agent 3] MEDIUM RISK                   │
│ ... (rest of team)                      │
├─────────────────────────────────────────┤
│ [Team Analytics]                        │
│ - Top Performers                        │
│ - Activity Comparison Chart             │
│ - Team Trends                           │
└─────────────────────────────────────────┘
```

**Features:**
- Team overview metrics
- At-risk agent alerts
- Agent comparisons
- Team rankings
- Export team reports
- Quick action buttons (contact, coach)

---

### 3. Division Head Dashboard

**Layout:**
```
┌─────────────────────────────────────────┐
│ Division Overview - [Division Name]     │
├─────────────────────────────────────────┤
│ [Division Summary Cards]                │
│ - Total Areas: 5                        │
│ - Total Agents: 42                      │
│ - Division Target: $25M                 │
│ - Current Sales: $18.5M (74%)           │
│ - At Risk Agents: 12                    │
├─────────────────────────────────────────┤
│ [Area Performance Cards]                │
│ [Area 1] Target: 82% | 8 Agents         │
│ [Area 2] Target: 76% | 9 Agents         │
│ [Area 3] Target: 68% | 7 Agents         │
│ [Area 4] Target: 71% | 10 Agents        │
│ [Area 5] Target: 65% | 8 Agents         │
├─────────────────────────────────────────┤
│ [Executive Insights]                    │
│ - Top Performing Area                   │
│ - Areas Needing Support                 │
│ - Division Trends                       │
│ - Forecast vs Actual                    │
├─────────────────────────────────────────┤
│ [Quick Actions]                         │
│ - View All Agents                       │
│ - Area Comparison Report                │
│ - Export Division Report                │
└─────────────────────────────────────────┘
```

**Features:**
- Division-wide metrics
- Area comparisons
- Performance heatmap
- Trend analysis
- Executive reports
- Drill-down capability

---

## 🗄️ Database Schema Updates

### New Collections:

#### `users`
```javascript
{
  "_id": "U001",
  "username": "maria.santos",
  "email": "maria@company.com",
  "password": "hashed_password",
  "role": "agent|area_manager|division_head",
  "agent_id": "A101", // if role is agent
  "area_id": "AR001", // if role is area_manager
  "division_id": "DIV001", // if role is division_head
  "created_at": "2024-01-01"
}
```

#### `areas`
```javascript
{
  "_id": "AR001",
  "name": "North Region",
  "division_id": "DIV001",
  "manager_id": "U005",
  "monthly_target": 4800000,
  "created_at": "2024-01-01"
}
```

#### `divisions`
```javascript
{
  "_id": "DIV001",
  "name": "Western Division",
  "head_id": "U010",
  "monthly_target": 25000000,
  "created_at": "2024-01-01"
}
```

### Updated `agents` Collection:
```javascript
{
  "_id": "A101",
  "name": "Maria Santos",
  "email": "maria@company.com",
  "user_id": "U001", // Link to user account
  "area_id": "AR001", // Which area they belong to
  "monthly_target": 600000,
  "created_at": "2024-01-01"
}
```

---

## 🔐 Authentication & Authorization

### Access Control Matrix

| Feature | Agent | Area Manager | Division Head |
|---------|-------|--------------|---------------|
| View own data | ✅ | ✅ | ✅ |
| View team agents | ❌ | ✅ | ✅ |
| View all areas | ❌ | ❌ | ✅ |
| Edit own data | ✅ | ✅ | ✅ |
| Edit team data | ❌ | ✅ | ✅ |
| View division reports | ❌ | ❌ | ✅ |
| Train AI model | ❌ | ✅ | ✅ |
| Manage users | ❌ | ❌ | ✅ |

---

## 📱 URL Structure

```
/ → Login page (redirects based on role)

Agent Routes:
/agent/dashboard → Agent's personal dashboard
/agent/performance → Detailed performance view
/agent/goals → Personal goals and targets

Area Manager Routes:
/area-manager/dashboard → Team overview
/area-manager/team → Detailed team view
/area-manager/agent/<id> → Individual agent view
/area-manager/reports → Team reports

Division Head Routes:
/division-head/dashboard → Division overview
/division-head/areas → All areas comparison
/division-head/area/<id> → Specific area view
/division-head/reports → Executive reports
/division-head/analytics → Division analytics
```

---

## 🎨 Design Consistency

All dashboards will use the same minimalist design system:
- Clean white cards
- Subtle borders
- Gray/black color palette
- Consistent typography
- Risk color coding (red/orange/green)
- Responsive layout

---

## 📈 Key Metrics by Role

### Agent Metrics:
- Personal sales vs target
- Activity counts
- Daily/weekly trends
- Team ranking
- Improvement suggestions

### Area Manager Metrics:
- Team total sales
- Team average performance
- At-risk agent count
- Team activity levels
- Area ranking in division

### Division Head Metrics:
- Division total sales
- Area performance comparison
- Division trends
- Resource allocation insights
- Strategic KPIs

---

## 🔔 Notification System

### Alerts by Role:

**Agents:**
- Daily progress updates
- Target milestone alerts
- Performance dips

**Area Managers:**
- High-risk agent alerts
- Team target warnings
- Daily team summary

**Division Heads:**
- Weekly division summary
- Area performance alerts
- Strategic insights

---

## 📊 Reporting Features

### Agent Reports:
- Personal performance report (PDF)
- Activity log (CSV)
- Monthly summary

### Area Manager Reports:
- Team performance report (PDF)
- Agent comparison spreadsheet (Excel)
- Weekly team summary (PDF)

### Division Head Reports:
- Executive dashboard (PDF)
- Division analytics (PowerPoint)
- Area comparison matrix (Excel)
- Strategic insights report (PDF)

---

## 🚀 Implementation Priority

### Phase 1: Core Hierarchy (Now)
1. Create user, area, division models
2. Update agent model with area_id
3. Implement basic authentication
4. Create role-based routing

### Phase 2: Dashboards (Next)
5. Build agent dashboard
6. Build area manager dashboard
7. Build division head dashboard
8. Implement access control

### Phase 3: Advanced Features (Later)
9. Add comparison features
10. Implement notifications
11. Create report exports
12. Add analytics charts

---

## 💡 Additional Features

### Gamification:
- Leaderboards by area
- Achievement badges
- Performance streaks
- Monthly top performer awards

### Collaboration:
- Internal messaging
- Team chat
- Performance notes
- Coaching logs

### Analytics:
- Predictive forecasting
- Trend analysis
- What-if scenarios
- Resource optimization

---

## 🎯 Success Metrics

**For Agents:**
- Improved individual performance
- Better goal awareness
- More proactive behavior

**For Area Managers:**
- Earlier intervention for at-risk agents
- Better team coordination
- Improved coaching effectiveness

**For Division Heads:**
- Better strategic decisions
- Resource optimization
- Division-wide improvements

---

**This hierarchical system transforms the application from a simple tracking tool into a comprehensive enterprise sales management platform!**

Would you like me to start implementing this multi-level system?
