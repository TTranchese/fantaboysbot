# Telegram Formation Management Bot

## Overview

This is a Telegram bot designed for managing team formations with time-restricted submissions and administrative oversight. The bot enforces specific submission windows (17:00-19:00), requires private message submissions, and provides admin-only access to view all submitted formations. The system uses in-memory storage for temporary session-based data persistence and includes comprehensive error handling for unauthorized access and time violations.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Bot Framework
- **Technology**: Python with pyTeleBot library
- **Rationale**: Provides simple, synchronous bot development with built-in message handling decorators
- **Design Pattern**: Event-driven message handlers with command-based routing

### Access Control System
- **Time-Based Restrictions**: Submissions only accepted between 17:00-19:00 daily
- **Privacy Enforcement**: All formation submissions must be sent via private messages to the bot
- **Admin Authorization**: Only designated admin users can view all submitted formations
- **Rationale**: Ensures controlled submission windows and maintains privacy of individual formations

### Data Storage
- **Architecture**: In-memory dictionary storage (`formazioni = {}`)
- **Scope**: Session-based temporary storage that resets on bot restart
- **Rationale**: Simple implementation for temporary data that doesn't require persistence across sessions
- **Trade-offs**: Data loss on restart but eliminates database complexity for temporary use cases

### Message Processing
- **Handler Structure**: Decorator-based message handlers for different command types
- **Error Handling**: Comprehensive feedback system for various violation scenarios
- **Logging**: Structured logging with timestamp, level, and context information

### Configuration Management
- **Environment Variables**: Bot token and admin username stored as environment variables
- **Fallback Values**: Default configuration values provided for development/testing
- **Security**: Sensitive tokens externalized from codebase

## External Dependencies

### Telegram Bot API
- **Service**: Telegram's Bot API platform
- **Purpose**: Core messaging infrastructure and bot hosting
- **Integration**: Via pyTeleBot Python wrapper library

### Python Libraries
- **pyTeleBot**: Main Telegram bot framework for message handling and API communication
- **datetime**: Built-in Python module for time-based restrictions and scheduling
- **logging**: Built-in Python module for structured application logging
- **os**: Built-in Python module for environment variable access

### Runtime Environment
- **Python 3.x**: Required runtime environment
- **Environment Variables**: TELEGRAM_BOT_TOKEN and ADMIN_USERNAME for bot configuration