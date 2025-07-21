import { useState } from 'react'

interface FormData {
  company_name: string
  website: string
  linkedin: string
  pitch_deck: string
  github?: string
  email: string
  meeting_time: string
}

export default function App() {
  const [form, setForm] = useState<FormData>({
    company_name: '',
    website: '',
    linkedin: '',
    pitch_deck: '',
    github: '',
    email: '',
    meeting_time: ''
  })
  const [status, setStatus] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)
    setStatus('Submitting...')
    
    // Format datetime to readable string
    const formatDateTime = (datetime: string) => {
      if (!datetime) return ''
      const date = new Date(datetime)
      return date.toLocaleString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long', 
        day: 'numeric',
        hour: 'numeric',
        minute: '2-digit',
        timeZoneName: 'short'
      })
    }

    // Validate and format URLs
    const formData = {
      ...form,
      website: form.website.startsWith('http') ? form.website : `https://${form.website}`,
      pitch_deck: form.pitch_deck.startsWith('http') ? form.pitch_deck : `https://${form.pitch_deck}`,
      github: form.github && form.github.trim() ? 
        (form.github.startsWith('http') ? form.github : `https://${form.github}`) : 
        undefined,
      meeting_time: formatDateTime(form.meeting_time)
    }
    
    try {
      const res = await fetch('http://localhost:8000/api/apply', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      })
      
      if (res.ok) {
        const data = await res.json()
        setStatus(`✅ Scheduled! Zoom link: ${data.zoom}`)
        // Clear form on success
        setForm({
          company_name: '',
          website: '',
          linkedin: '',
          pitch_deck: '',
          github: '',
          email: '',
          meeting_time: ''
        })
      } else {
        const errorData = await res.json()
        setStatus(`❌ Error: ${errorData.detail || 'Please try again.'}`)
      }
    } catch (error) {
      setStatus('❌ Connection error. Please ensure the backend server is running.')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%)',
      color: '#ffffff',
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
      padding: '0',
      margin: '0'
    }}>
      {/* Background decoration */}
      <div style={{
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        background: `
          radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.1) 0%, transparent 50%),
          radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.1) 0%, transparent 50%),
          radial-gradient(circle at 40% 40%, rgba(120, 200, 255, 0.05) 0%, transparent 50%)
        `,
        pointerEvents: 'none'
      }} />
      
      <div style={{
        position: 'relative',
        zIndex: 1,
        maxWidth: '600px',
        margin: '0 auto',
        padding: '60px 20px'
      }}>
        {/* Header */}
        <div style={{ textAlign: 'center', marginBottom: '50px' }}>
          <h1 style={{
            fontSize: '3.5rem',
            fontWeight: '700',
            margin: '0 0 20px 0',
            background: 'linear-gradient(135deg, #fff 0%, #a78bfa 50%, #06b6d4 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text'
          }}>
            Practice Pitch
          </h1>
          <p style={{
            fontSize: '1.25rem',
            color: '#94a3b8',
            lineHeight: '1.6',
            margin: '0',
            maxWidth: '500px',
            marginLeft: 'auto',
            marginRight: 'auto'
          }}>
            Perfect your startup pitch with our AI-powered VC bot. Get real feedback before the real meeting.
          </p>
        </div>

        {/* Form Card */}
        <div style={{
          background: 'rgba(255, 255, 255, 0.05)',
          border: '1px solid rgba(255, 255, 255, 0.1)',
          borderRadius: '16px',
          padding: '40px',
          backdropFilter: 'blur(10px)',
          boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25)'
        }}>
          <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
              <div style={{ gridColumn: '1 / -1' }}>
                <label style={{
                  display: 'block',
                  fontSize: '0.875rem',
                  fontWeight: '500',
                  color: '#e2e8f0',
                  marginBottom: '8px'
                }}>
                  Company Name *
                </label>
                <input 
                  name="company_name" 
                  placeholder="Enter your company name"
                  value={form.company_name} 
                  onChange={handleChange} 
                  required 
                  className="form-input"
                />
              </div>
              
              <div>
                <label style={{
                  display: 'block',
                  fontSize: '0.875rem',
                  fontWeight: '500',
                  color: '#e2e8f0',
                  marginBottom: '8px'
                }}>
                  Website *
                </label>
                <input 
                  name="website" 
                  placeholder="https://yourcompany.com"
                  value={form.website} 
                  onChange={handleChange} 
                  required 
                  className="form-input"
                />
              </div>

              <div>
                <label style={{
                  display: 'block',
                  fontSize: '0.875rem',
                  fontWeight: '500',
                  color: '#e2e8f0',
                  marginBottom: '8px'
                }}>
                  Founder's LinkedIn *
                </label>
                <input 
                  name="linkedin" 
                  placeholder="linkedin.com/in/founder"
                  value={form.linkedin} 
                  onChange={handleChange} 
                  required 
                  className="form-input"
                />
              </div>

              <div style={{ gridColumn: '1 / -1' }}>
                <label style={{
                  display: 'block',
                  fontSize: '0.875rem',
                  fontWeight: '500',
                  color: '#e2e8f0',
                  marginBottom: '8px'
                }}>
                  Pitch Deck URL *
                </label>
                <input 
                  name="pitch_deck" 
                  placeholder="Link to your pitch deck (Google Drive, Dropbox, etc.)"
                  value={form.pitch_deck} 
                  onChange={handleChange} 
                  required 
                  className="form-input"
                />
              </div>

              <div>
                <label style={{
                  display: 'block',
                  fontSize: '0.875rem',
                  fontWeight: '500',
                  color: '#e2e8f0',
                  marginBottom: '8px'
                }}>
                  GitHub (Optional)
                </label>
                <input 
                  name="github" 
                  placeholder="github.com/yourcompany"
                  value={form.github} 
                  onChange={handleChange} 
                  className="form-input"
                />
              </div>

              <div>
                <label style={{
                  display: 'block',
                  fontSize: '0.875rem',
                  fontWeight: '500',
                  color: '#e2e8f0',
                  marginBottom: '8px'
                }}>
                  Contact Email *
                </label>
                <input 
                  name="email" 
                  type="email"
                  placeholder="founder@company.com"
                  value={form.email} 
                  onChange={handleChange} 
                  required 
                  className="form-input"
                />
              </div>

              <div style={{ gridColumn: '1 / -1' }}>
                <label style={{
                  display: 'block',
                  fontSize: '0.875rem',
                  fontWeight: '500',
                  color: '#e2e8f0',
                  marginBottom: '8px'
                }}>
                  Preferred Meeting Time *
                </label>
                <input 
                  name="meeting_time" 
                  type="datetime-local"
                  value={form.meeting_time} 
                  onChange={handleChange} 
                  required 
                  min={new Date().toISOString().slice(0, 16)} // Prevent past dates
                  step="1800" // 30 minutes in seconds (30 * 60 = 1800)
                  className="form-input"
                  style={{
                    colorScheme: 'dark', // Makes the datetime picker dark themed
                    cursor: 'pointer' // Show pointer cursor for entire input
                  }}
                  onClick={(e) => {
                    // Make entire input clickable to open picker
                    e.currentTarget.showPicker?.()
                  }}
                />
              </div>
            </div>

            <button 
              type="submit" 
              disabled={isSubmitting}
              style={{
                width: '100%',
                padding: '16px',
                borderRadius: '8px',
                border: 'none',
                background: isSubmitting 
                  ? 'rgba(167, 139, 250, 0.5)' 
                  : 'linear-gradient(135deg, #a78bfa 0%, #06b6d4 100%)',
                color: '#ffffff',
                fontSize: '1.1rem',
                fontWeight: '600',
                cursor: isSubmitting ? 'not-allowed' : 'pointer',
                transition: 'all 0.2s ease',
                transform: isSubmitting ? 'scale(0.98)' : 'scale(1)',
                boxShadow: isSubmitting 
                  ? 'none' 
                  : '0 10px 25px -12px rgba(167, 139, 250, 0.4)'
              }}
              onMouseEnter={(e) => {
                if (!isSubmitting) {
                  const target = e.target as HTMLButtonElement
                  target.style.transform = 'translateY(-2px)'
                  target.style.boxShadow = '0 15px 35px -12px rgba(167, 139, 250, 0.6)'
                }
              }}
              onMouseLeave={(e) => {
                if (!isSubmitting) {
                  const target = e.target as HTMLButtonElement
                  target.style.transform = 'translateY(0)'
                  target.style.boxShadow = '0 10px 25px -12px rgba(167, 139, 250, 0.4)'
                }
              }}
            >
              {isSubmitting ? '⏳ Scheduling...' : '🚀 Schedule Practice Session'}
            </button>
          </form>

          {status && (
            <div style={{
              marginTop: '24px',
              padding: '16px',
              borderRadius: '8px',
              background: status.includes('✅') 
                ? 'rgba(34, 197, 94, 0.1)' 
                : 'rgba(239, 68, 68, 0.1)',
              border: `1px solid ${status.includes('✅') ? 'rgba(34, 197, 94, 0.3)' : 'rgba(239, 68, 68, 0.3)'}`,
              color: status.includes('✅') ? '#4ade80' : '#f87171',
              fontSize: '1rem',
              textAlign: 'center'
            }}>
              {status}
            </div>
          )}
        </div>

        {/* Footer */}
        <div style={{
          textAlign: 'center',
          marginTop: '40px',
          color: '#64748b',
          fontSize: '0.875rem'
        }}>
          <p>Practice makes perfect. Get feedback that matters.</p>
        </div>
      </div>
    </div>
  )
}
