"""
Unit tests for the email sender module.
"""

import pytest
import smtplib
from unittest.mock import Mock, patch, MagicMock
from src.agent.email_sender import EmailSender


class TestEmailSender:
    """Test cases for EmailSender class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.email_config = {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'email': 'test@gmail.com',
            'password': 'test_password'
        }
        self.sender = EmailSender(**self.email_config)
    
    def test_init(self):
        """Test initialization of EmailSender"""
        assert self.sender.smtp_server == 'smtp.gmail.com'
        assert self.sender.smtp_port == 587
        assert self.sender.email == 'test@gmail.com'
        assert self.sender.password == 'test_password'
    
    @patch('smtplib.SMTP')
    def test_send_email_success(self, mock_smtp):
        """Test successful email sending"""
        # Mock SMTP server
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        # Test data
        to_email = 'recipient@example.com'
        subject = 'Test Subject'
        body = '<html><body>Test body</body></html>'
        
        # Call method
        result = self.sender.send_email(to_email, subject, body)
        
        # Verify results
        assert result == True
        mock_smtp.assert_called_once_with('smtp.gmail.com', 587)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with('test@gmail.com', 'test_password')
        mock_server.sendmail.assert_called_once()
        mock_server.quit.assert_called_once()
    
    @patch('smtplib.SMTP')
    def test_send_email_auth_failure(self, mock_smtp):
        """Test email authentication failure"""
        # Mock SMTP server with auth error
        mock_server = MagicMock()
        mock_server.login.side_effect = smtplib.SMTPAuthenticationError(535, 'Authentication failed')
        mock_smtp.return_value = mock_server
        
        # Test data
        to_email = 'recipient@example.com'
        subject = 'Test Subject'
        body = 'Test body'
        
        # Call method
        result = self.sender.send_email(to_email, subject, body)
        
        # Verify results
        assert result == False
        mock_server.login.assert_called_once()
    
    @patch('smtplib.SMTP')
    def test_send_email_general_error(self, mock_smtp):
        """Test general email sending error"""
        # Mock SMTP server with general error
        mock_smtp.side_effect = Exception("Connection failed")
        
        # Test data
        to_email = 'recipient@example.com'
        subject = 'Test Subject'
        body = 'Test body'
        
        # Call method
        result = self.sender.send_email(to_email, subject, body)
        
        # Verify results
        assert result == False
    
    @patch('smtplib.SMTP')
    def test_send_email_html_content(self, mock_smtp):
        """Test sending HTML email content"""
        # Mock SMTP server
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        # Test HTML content
        html_body = """
        <html>
        <head><title>Test</title></head>
        <body>
            <h1>Test Newsletter</h1>
            <p>This is a test email with HTML content.</p>
        </body>
        </html>
        """
        
        # Call method
        result = self.sender.send_email('test@example.com', 'HTML Test', html_body)
        
        # Verify success
        assert result == True
        mock_server.sendmail.assert_called_once() 