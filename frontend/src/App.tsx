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

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setStatus('Submitting...')
    const res = await fetch('http://localhost:8000/api/apply', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form)
    })
    if (res.ok) {
      const data = await res.json()
      setStatus('Scheduled! Zoom link: ' + data.zoom)
    } else {
      setStatus('Error submitting form')
    }
  }

  return (
    <div>
      <h1>Practice Pitch</h1>
      <p>Fill out the form below to schedule a practice session with our VC bot.</p>
      <form onSubmit={handleSubmit}>
        <input name="company_name" placeholder="Company Name" value={form.company_name} onChange={handleChange} required />
        <input name="website" placeholder="Website" value={form.website} onChange={handleChange} required />
        <input name="linkedin" placeholder="Founders LinkedIn" value={form.linkedin} onChange={handleChange} required />
        <input name="pitch_deck" placeholder="Pitch Deck URL" value={form.pitch_deck} onChange={handleChange} required />
        <input name="github" placeholder="GitHub (optional)" value={form.github} onChange={handleChange} />
        <input name="email" placeholder="Contact Email" value={form.email} onChange={handleChange} required />
        <input name="meeting_time" placeholder="Preferred Time" value={form.meeting_time} onChange={handleChange} required />
        <button type="submit">Schedule</button>
      </form>
      <p>{status}</p>
    </div>
  )
}
