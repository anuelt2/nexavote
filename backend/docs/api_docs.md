# NexaVote API Documentation

## Overview

NexaVote is a secure electronic voting platform that enables organizations to conduct transparent, verifiable elections. The platform uses invite-only registration and provides comprehensive voting management capabilities.

**Base URL:** `https://api.nexavote.com/`
**API Version:** v1
**Authentication:** Token-based authentication required for most endpoints

## Quick Start

1. **Get an invitation:** Elections are invite-only. An admin must send you an invitation email.
2. **Register:** Use the token from your invitation email to register your account.
3. **Login:** Authenticate to receive your API token.
4. **Vote:** Cast your votes in active elections.
5. **Verify:** Verify your vote using the returned vote hash.

## Authentication

### Overview
NexaVote uses Django's built-in authentication with token-based API access. Most endpoints require authentication.

### Headers
Include your authentication token in all API requests:
```
Authorization: Token your_token_here
```

### User Types
- **Voter**: Regular users who can vote in elections
- **Admin**: Users who can create elections, candidates, and manage the platform
- **Staff**: Administrative users with limited permissions

## API Endpoints

### Root Endpoint

#### GET /
Returns all available API endpoints and their URLs.

**Response:**
```json
{
  "admin": "/admin/",
  "home": "/",
  "register": "/api/users/register/voter/",
  "invitations": "/api/invitations/create/",
  "election-events": "/api/election-events/",
  "elections": "/api/elections/",
  "candidates": "/api/candidates/",
  "cast-vote": "/api/votes/",
  "my-votes": "/api/votes/my-votes/",
  "verify-vote": "/api/votes/verify/",
  "audit-logs": "/api/votes/audit-logs/"
}
```

## User Management

### Register Voter via Token

#### POST /api/users/register/voter/
Register a new voter account using an invitation token.

**Request Body:**
```json
{
  "token": "invitation_token_here",
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password123",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response (201 Created):**
```json
{
  "message": "Voter registration successful"
}
```

**Error Response (400 Bad Request):**
```json
{
  "token": ["Invalid or expired token"],
  "email": ["User with this email already exists"]
}
```

### Register Admin/Staff

#### POST /api/users/register/admin-staff/
Register admin or staff users (Admin only).

**Authentication:** Required (Admin only)

**Request Body:**
```json
{
  "username": "admin_user",
  "email": "admin@example.com",
  "password": "secure_password123",
  "first_name": "Admin",
  "last_name": "User",
  "user_type": "admin"
}
```

**Response (201 Created):**
```json
{
  "message": "Admin/Staff registration successful"
}
```

## Invitation Management

### Create Invitation

#### POST /api/invitations/create/
Create and send voter invitations (Admin only).

**Authentication:** Required (Admin only)

**Request Body:**
```json
{
  "email": "voter@example.com",
  "election_event": "uuid-of-election-event",
  "first_name": "Jane",
  "last_name": "Doe"
}
```

**Response (201 Created):**
```json
{
  "id": "invitation-uuid",
  "email": "voter@example.com",
  "election_event": "uuid-of-election-event",
  "token": "unique-invitation-token",
  "is_used": false,
  "created_at": "2024-01-15T10:30:00Z"
}
```

## Election Events

### List Election Events

#### GET /api/election-events/
Retrieve all election events.

**Authentication:** Required

**Response (200 OK):**
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "event-uuid-1",
      "title": "Student Council Elections 2024",
      "description": "Annual student council elections",
      "start_date": "2024-02-01T09:00:00Z",
      "end_date": "2024-02-03T17:00:00Z",
      "is_active": true,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

## Elections

### List Elections

#### GET /api/elections/
Retrieve elections, optionally filtered by election event.

**Authentication:** Required

**Query Parameters:**
- `event` (optional): Filter by election event UUID

**Example Request:**
```
GET /api/elections/?event=event-uuid-1
```

**Response (200 OK):**
```json
{
  "count": 1,
  "results": [
    {
      "id": "election-uuid-1",
      "title": "Student Council President",
      "description": "Election for student council president position",
      "election_event": "event-uuid-1",
      "start_time": "2024-02-01T09:00:00Z",
      "end_time": "2024-02-03T17:00:00Z",
      "is_active": true,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

### Create Election (Admin)

#### POST /api/elections/admin/
Create a new election (Admin only).

**Authentication:** Required (Admin only)

**Request Body:**
```json
{
  "title": "Class Representative",
  "description": "Election for class representative",
  "election_event": "event-uuid-1",
  "start_time": "2024-02-01T09:00:00Z",
  "end_time": "2024-02-03T17:00:00Z"
}
```

**Response (201 Created):**
```json
{
  "id": "new-election-uuid",
  "title": "Class Representative",
  "description": "Election for class representative",
  "election_event": "event-uuid-1",
  "start_time": "2024-02-01T09:00:00Z",
  "end_time": "2024-02-03T17:00:00Z",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Update/Delete Election (Admin)

#### GET/PUT/PATCH/DELETE /api/elections/admin/{election_id}/
Retrieve, update, or delete a specific election (Admin only).

**Authentication:** Required (Admin only)

**Update Request Body (PUT/PATCH):**
```json
{
  "title": "Updated Election Title",
  "description": "Updated description",
  "start_time": "2024-02-01T09:00:00Z",
  "end_time": "2024-02-03T17:00:00Z"
}
```

## Candidates

### List Candidates

#### GET /api/candidates/
Retrieve candidates, optionally filtered by election.

**Authentication:** Required

**Query Parameters:**
- `election` (optional): Filter by election UUID

**Example Request:**
```
GET /api/candidates/?election=election-uuid-1
```

**Response (200 OK):**
```json
{
  "count": 2,
  "results": [
    {
      "id": "candidate-uuid-1",
      "first_name": "Alice",
      "last_name": "Johnson",
      "email": "alice@example.com",
      "bio": "Experienced student leader",
      "election": "election-uuid-1",
      "created_at": "2024-01-15T10:30:00Z"
    },
    {
      "id": "candidate-uuid-2",
      "first_name": "Bob",
      "last_name": "Smith",
      "email": "bob@example.com",
      "bio": "Dedicated to student welfare",
      "election": "election-uuid-1",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

### Create Candidate (Admin)

#### POST /api/candidates/admin/
Create a new candidate (Admin only).

**Authentication:** Required (Admin only)

**Request Body:**
```json
{
  "first_name": "Charlie",
  "last_name": "Brown",
  "email": "charlie@example.com",
  "bio": "Future leader with fresh ideas",
  "election": "election-uuid-1"
}
```

**Response (201 Created):**
```json
{
  "id": "new-candidate-uuid",
  "first_name": "Charlie",
  "last_name": "Brown",
  "email": "charlie@example.com",
  "bio": "Future leader with fresh ideas",
  "election": "election-uuid-1",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Update/Delete Candidate (Admin)

#### GET/PUT/PATCH/DELETE /api/candidates/admin/{candidate_id}/
Retrieve, update, or delete a specific candidate (Admin only).

**Authentication:** Required (Admin only)

## Voting

### Cast Vote

#### POST /api/votes/
Cast a vote for a candidate.

**Authentication:** Required (Voter only)

**Request Body:**
```json
{
  "candidate_id": "candidate-uuid-1"
}
```

**Response (201 Created):**
```json
{
  "id": "vote-uuid",
  "vote_hash": "abc123def456...",
  "candidate_name": "Alice Johnson",
  "election_title": "Student Council President",
  "created_at": "2024-02-01T14:30:00Z",
  "is_verified": true
}
```

**Error Responses:**
- **400 Bad Request:** Already voted in this election
- **400 Bad Request:** Election is not currently open
- **404 Not Found:** Invalid candidate ID

### Get My Votes

#### GET /api/votes/my-votes/
Retrieve all votes cast by the authenticated user.

**Authentication:** Required

**Response (200 OK):**
```json
{
  "count": 2,
  "results": [
    {
      "id": "vote-uuid-1",
      "voter_email": "john@example.com",
      "candidate_name": "Alice Johnson",
      "election_title": "Student Council President",
      "election_id": "election-uuid-1",
      "vote_hash": "abc123def456...",
      "is_verified": true,
      "created_at": "2024-02-01T14:30:00Z"
    }
  ]
}
```

### Verify Vote

#### POST /api/votes/verify/
Verify a vote using its hash.

**Authentication:** Required

**Request Body:**
```json
{
  "vote_hash": "abc123def456..."
}
```

**Response (200 OK):**
```json
{
  "verified": true,
  "vote_id": "vote-uuid",
  "election_title": "Student Council President",
  "candidate_name": "Alice Johnson",
  "created_at": "2024-02-01T14:30:00Z",
  "is_verified": true
}
```

**Error Response (404 Not Found):**
```json
{
  "verified": false,
  "message": "Vote hash not found"
}
```

### Check Vote Status

#### GET /api/votes/check-status/{election_id}/
Check if the authenticated user has voted in a specific election.

**Authentication:** Required

**Response (200 OK):**
```json
{
  "has_voted": true,
  "election_id": "election-uuid-1",
  "election_title": "Student Council President",
  "election_status": "active"
}
```

### Get Election Results

#### GET /api/votes/results/{election_id}/
Get results for a specific election (only available after election ends or to admins).

**Authentication:** Required

**Response (200 OK):**
```json
{
  "election_id": "election-uuid-1",
  "election_title": "Student Council President",
  "total_votes": 150,
  "results": [
    {
      "candidate_name": "Alice Johnson",
      "vote_count": 85
    },
    {
      "candidate_name": "Bob Smith",
      "vote_count": 65
    }
  ]
}
```

### Get Election Statistics (Admin)

#### GET /api/votes/statistics/{election_id}/
Get detailed statistics for a specific election (Admin only).

**Authentication:** Required (Admin only)

**Response (200 OK):**
```json
{
  "election_id": "election-uuid-1",
  "election_title": "Student Council President",
  "total_votes": 150,
  "candidate_results": [
    {
      "candidate__first_name": "Alice",
      "candidate__last_name": "Johnson",
      "vote_count": 85
    }
  ],
  "voting_timeline": [
    {
      "hour": "2024-02-01T09:00:00Z",
      "vote_count": 25
    }
  ],
  "verification_stats": {
    "verified_votes": 148,
    "unverified_votes": 2
  }
}
```

### Get Audit Logs (Admin)

#### GET /api/votes/audit-logs/
Retrieve vote audit logs (Admin only).

**Authentication:** Required (Admin only)

**Query Parameters:**
- `action` (optional): Filter by action type (cast, verify, etc.)
- `vote__candidate__election` (optional): Filter by election UUID

**Response (200 OK):**
```json
{
  "count": 10,
  "results": [
    {
      "id": "log-uuid-1",
      "action": "cast",
      "performed_by_email": "john@example.com",
      "details": "Vote cast for candidate Alice Johnson",
      "ip_address": "192.168.1.100",
      "created_at": "2024-02-01T14:30:00Z",
      "vote_details": {
        "vote_id": "vote-uuid-1",
        "voter_email": "john@example.com",
        "candidate_name": "Alice Johnson",
        "election_title": "Student Council President"
      }
    }
  ]
}
```

## Error Handling

### Common HTTP Status Codes

- **200 OK**: Request successful
- **201 Created**: Resource created successfully
- **400 Bad Request**: Invalid request data
- **401 Unauthorized**: Authentication required
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server error

### Error Response Format

All error responses follow this format:
```json
{
  "field_name": ["Error message"],
  "non_field_errors": ["General error message"]
}
```

### Common Error Scenarios

1. **Already Voted**: Users can only vote once per election
2. **Election Closed**: Cannot vote in inactive elections
3. **Invalid Token**: Registration tokens are one-time use
4. **Permission Denied**: Admin-only endpoints require admin permissions
5. **Invalid Vote Hash**: Vote verification requires valid hash

## Rate Limiting

- **General API**: 100 requests per hour per user
- **Vote Casting**: 10 requests per hour per user
- **Authentication**: 20 requests per hour per IP

## Security Features

### Vote Integrity
- Each vote generates a unique hash for verification
- One vote per user per election enforced at database level
- Audit logging for all vote-related actions

### Data Protection
- All sensitive data encrypted at rest
- HTTPS required for all API communications
- IP address logging for security monitoring

### Access Control
- Role-based permissions (Voter, Admin, Staff)
- Token-based authentication
- Invite-only registration system

## Best Practices

### For Developers

1. **Always authenticate**: Most endpoints require authentication
2. **Handle errors gracefully**: Check response status codes
3. **Verify votes**: Use the vote hash to verify successful vote casting
4. **Respect rate limits**: Implement proper retry logic
5. **Use HTTPS**: Never send requests over HTTP

### For Administrators

1. **Test elections**: Create test elections before live events
2. **Monitor audit logs**: Regularly check for suspicious activity
3. **Backup data**: Ensure vote data is properly backed up
4. **Verify results**: Cross-check results using multiple methods

## SDKs and Libraries

### Python SDK Example
```python
import requests

class NexaVoteAPI:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.headers = {'Authorization': f'Token {token}'}
    
    def cast_vote(self, candidate_id):
        response = requests.post(
            f"{self.base_url}/api/votes/",
            json={"candidate_id": candidate_id},
            headers=self.headers
        )
        return response.json()
    
    def verify_vote(self, vote_hash):
        response = requests.post(
            f"{self.base_url}/api/votes/verify/",
            json={"vote_hash": vote_hash},
            headers=self.headers
        )
        return response.json()

# Usage
api = NexaVoteAPI("https://api.nexavote.com", "your-token-here")
result = api.cast_vote("candidate-uuid-here")
print(f"Vote hash: {result['vote_hash']}")
```

### JavaScript SDK Example
```javascript
class NexaVoteAPI {
    constructor(baseUrl, token) {
        this.baseUrl = baseUrl;
        this.headers = {
            'Authorization': `Token ${token}`,
            'Content-Type': 'application/json'
        };
    }
    
    async castVote(candidateId) {
        const response = await fetch(`${this.baseUrl}/api/votes/`, {
            method: 'POST',
            headers: this.headers,
            body: JSON.stringify({ candidate_id: candidateId })
        });
        return await response.json();
    }
    
    async verifyVote(voteHash) {
        const response = await fetch(`${this.baseUrl}/api/votes/verify/`, {
            method: 'POST',
            headers: this.headers,
            body: JSON.stringify({ vote_hash: voteHash })
        });
        return await response.json();
    }
}

// Usage
const api = new NexaVoteAPI('https://api.nexavote.com', 'your-token-here');
api.castVote('candidate-uuid-here').then(result => {
    console.log(`Vote hash: ${result.vote_hash}`);
});
```

## Changelog

### Version 1.0.0 (Current)
- Initial API release
- Basic voting functionality
- User management
- Election management
- Vote verification
- Audit logging

---

*Last updated: Jully 2025*