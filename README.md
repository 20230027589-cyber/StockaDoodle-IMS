# StockaDoodle: Inventory Management System

**XAVIER UNIVERSITY – ATENEO DE CAGAYAN**  
**College of Computer Studies**  
**Department of Information Technology**  

---


## 👥 Team Members

| Name | GitHub Profile |
|------|----------------|
| Gerfel Jay C. Jimenez | [@your-github-username-here](https://github.com/your-github-username-here) |
| Ivan Risan O. Llenares | [@your-github-username-here](https://github.com/your-github-username-here) |
| Kent Xylle Ryz J. Romarate | [@your-github-username-here](https://github.com/your-github-username-here) |
| Noel Jose C. Villalveto | [@thirdyady](https://github.com/thirdyady) |

> 📝 *Each member should edit their forked copy of this file to add their actual GitHub username link, then create a Pull Request to the leader’s repo.*

---

## 🧩 System Overview

### 🔹 Basic Operations
- **Retailers**:  
  Use the POS module to record sales. Product stocks update automatically after each transaction. Includes gamification (daily quota & streaks).

- **Managers**:  
  View visual sales dashboards (Bar & Pie charts), perform stock maintenance, and receive low-stock or expiration alerts.

- **Admins**:  
  Manage user accounts and maintain database integrity. Use Multi-Factor Authentication (MFA) for enhanced security.

---

## 🧾 Information Needs (Reports)

The system generates the following reports:
1. **Sales Performance Report**
2. **Category Distribution Report**
3. **Retailer Performance Report**
4. **Low-Stock and Expiration Alert Report**
5. **Managerial Activity Log Report**
6. **Detailed Sales Transaction Report**
7. **User Accounts Report**

---

## 🚀 Project Milestones

### **Milestone 1 (Nov Week 1): Project Setup & API Design**
**What we'll do:**  
Set up the project repository, define system scope, and identify key entities for StockaDoodle’s API.

**Deliverables:**  
- Completed `README.md` with team details and milestones  
- Defined problem statement and data model outline  
- Created basic Flask REST API folder structure  

**Checklists:**  
- [ ] Hold team meeting to finalize topic  
- [ ] Define database models (Products, Users, Sales, Logs)  
- [ ] Set up `app.py` for Flask  
- [ ] Commit and push to GitHub  

---

### **Milestone 2 (Nov Week 2): Database & Endpoints**
**What we'll do:**  
Develop initial SQLite database schema and implement CRUD endpoints for Products and Users.

**Deliverables:**  
- `database.db` file created  
- Endpoints for `/products` and `/users`  
- Documentation of each endpoint in `api.yaml`

**Checklists:**  
- [ ] Create models and database connection  
- [ ] Implement POST, GET, PUT, DELETE routes  
- [ ] Test endpoints using Postman  
- [ ] Commit and push to GitHub  

---

### **Milestone 3 (Nov Week 3): User Roles & Authentication**
**What we'll do:**  
Add authentication (Admin, Manager, Retailer) and role-based access control.

**Deliverables:**  
- Secure login and JWT authentication  
- Role-based API restrictions  
- Updated API documentation  

**Checklists:**  
- [ ] Add `/login` endpoint  
- [ ] Implement JWT tokens  
- [ ] Restrict routes by role  
- [ ] Commit and push updates  

---

### **Milestone 4 (Nov Week 4): Reports & Testing**
**What we'll do:**  
Generate sales and performance reports. Conduct system testing for reliability and accuracy.

**Deliverables:**  
- Reports endpoints (e.g., `/reports/sales`)  
- System testing results  
- Debug log cleanup  

**Checklists:**  
- [ ] Implement report endpoints  
- [ ] Validate calculations  
- [ ] Perform integration testing  
- [ ] Commit and push  

---

### **Milestone 5 (Dec Week 1): Final Integration & Documentation**
**What we'll do:**  
Finalize UI integration (if applicable) and ensure all APIs are functional and documented.

**Deliverables:**  
- Completed documentation (README, API, screenshots)  
- Stable final API release  
- Submission-ready project  

**Checklists:**  
- [ ] Merge all branches  
- [ ] Review code consistency  
- [ ] Write final documentation  
- [ ] Submit repository link on Moodle  

---


