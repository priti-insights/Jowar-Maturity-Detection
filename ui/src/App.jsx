
import { useEffect, useRef, useState } from 'react';
import {
  BrowserRouter,
  Routes,
  Route,
  NavLink,
  Link,
  Navigate,
  Outlet,
  useLocation,
  useNavigate
} from 'react-router-dom';

import './App.css';


function Navbar() {
  const navigate = useNavigate();
  const token = sessionStorage.getItem('jowarai_token');
  const storedUser = sessionStorage.getItem('jowarai_user');

  let user = null;

  try {
    user = storedUser ? JSON.parse(storedUser) : null;
  } catch {
    user = null;
  }

  const isLoggedIn = Boolean(token && user && user.role);

  function handleLogout() {
    sessionStorage.removeItem('jowarai_token');
    sessionStorage.removeItem('jowarai_user');
    navigate('/login', { replace: true });
  }

  return (
    <header className="navbar">
      <Link to="/" className="brand">
        <span className="brand-mark">
          <i className="bi bi-flower1" />
        </span>
        <span>Jowar<span className="brand-accent">AI</span></span>
      </Link>

      <nav>
        <NavLink to="/" end>Home</NavLink>
        <NavLink to="/about">About</NavLink>

        {isLoggedIn && (
          <>
            <NavLink to="/detect">Detection</NavLink>
            <NavLink to="/results">Results</NavLink>
            <NavLink to="/history">History</NavLink>

            {user.role === 'admin' && (
              <NavLink to="/admin">Admin</NavLink>
            )}

            <button
              type="button"
              className="button button-secondary"
              onClick={handleLogout}
            >
              <i className="bi bi-box-arrow-right" /> Logout
            </button>
          </>
        )}

        {!isLoggedIn && (
          <NavLink to="/login">Sign In</NavLink>
        )}
      </nav>
    </header>
  );
}

function Footer() {
  return (
    <footer className="footer">
      <span>JowarAI · Academic Prototype</span>
      <span>AI-assisted jowar maturity assessment</span>
    </footer>
  );
}

function Home() {
  return (
    <>
      <Navbar />
      <main>
        <section className="home-hero">
          <div className="hero-content">
            <span className="eyebrow">AI-BASED CROP ANALYSIS</span>
            <h1>
              Jowar Maturity
              <span>Detection System</span>
            </h1>
            <p>
              Detect jowar panicles using computer vision and explore
              maturity-stage predictions to support informed harvest decisions.
            </p>

            <div className="hero-buttons">
              <Link to="/detect" className="button button-primary">
                Start Detection <i className="bi bi-arrow-right" />
              </Link>
              <a href="#workflow" className="button button-secondary">
                How it works
              </a>
            </div>

            <div className="prototype-note">
              <i className="bi bi-info-circle" />
              Academic prototype. Predictions require validation.
            </div>
          </div>

          <div className="hero-illustration">
            <div className="illustration-circle">
              <i className="bi bi-flower1" />
            </div>
            <span className="illustration-label">JOWAR PANICLE</span>
            <h2>Crop intelligence, made simple.</h2>
            <p>Detection · Classification · Assessment</p>
          </div>
        </section>

        <section className="workflow" id="workflow">
          <div className="section-heading">
            <span className="eyebrow">THE WORKFLOW</span>
            <h2>Three simple steps</h2>
            <p>From an image to an AI-assisted assessment.</p>
          </div>

          <div className="workflow-grid">
            <article className="workflow-card">
              <span className="step-number">01</span>
              <i className="bi bi-camera" />
              <h3>Capture or upload</h3>
              <p>Provide an image of a jowar panicle.</p>
            </article>

            <article className="workflow-card">
              <span className="step-number">02</span>
              <i className="bi bi-bounding-box" />
              <h3>Detect and classify</h3>
              <p>Locate the panicle and estimate its maturity stage.</p>
            </article>

            <article className="workflow-card">
              <span className="step-number">03</span>
              <i className="bi bi-clipboard-check" />
              <h3>Review results</h3>
              <p>Inspect predictions and relevant confidence values.</p>
            </article>
          </div>
        </section>
      </main>
      <Footer />
    </>
  );
}

function About() {
  return (
    <>
      <Navbar />
      <main className="inner-page about-page">
        <section className="about-hero">
          <div className="about-hero-copy">
            <span className="eyebrow">ABOUT THE PROJECT</span>
            <h1>
              Understanding jowar.
              <span>Supporting better decisions.</span>
            </h1>
            <p>
              An AI-based academic project that uses computer vision
              to detect jowar panicles and support maturity-stage assessment.
            </p>
            <Link to="/detect" className="button button-primary">
              Explore Detection <i className="bi bi-arrow-right" />
            </Link>
          </div>

          <div className="about-hero-art">
            <div className="about-art-circle">
              <i className="bi bi-flower1" />
            </div>
            <span>COMPUTER VISION FOR AGRICULTURE</span>
          </div>
        </section>

        <section className="about-section">
          <div className="about-section-heading">
            <span className="eyebrow">PROJECT OVERVIEW</span>
            <h2>What are we building?</h2>
            <p>
              A system that identifies jowar panicles from images and
              provides a foundation for maturity classification.
            </p>
          </div>

          <div className="about-objective-grid">
            <article className="about-info-card">
              <div className="about-icon">
                <i className="bi bi-bullseye" />
              </div>
              <h3>Our objective</h3>
              <p>
                Detect jowar panicles using YOLO and use a separate image
                classifier to estimate the maturity stage.
              </p>
            </article>

            <article className="about-info-card">
              <div className="about-icon gold-icon">
                <i className="bi bi-lightbulb" />
              </div>
              <h3>Why it matters</h3>
              <p>
                Maturity assessment may help inform harvest decisions when
                supported by reliable data and validated agricultural criteria.
              </p>
            </article>
          </div>
        </section>

        <section className="about-section">
          <div className="about-section-heading">
            <span className="eyebrow">TECHNOLOGY STACK</span>
            <h2>Tools behind the system</h2>
          </div>

          <div className="about-tech-grid">
            <article className="about-tech-card">
              <i className="bi bi-eye" />
              <h3>YOLOv8</h3>
              <p>Panicle object detection</p>
            </article>
            <article className="about-tech-card">
              <i className="bi bi-code-slash" />
              <h3>Python</h3>
              <p>Model inference and processing</p>
            </article>
            <article className="about-tech-card">
              <i className="bi bi-image" />
              <h3>Image classification</h3>
              <p>Maturity-stage prediction</p>
            </article>
            <article className="about-tech-card">
              <i className="bi bi-window" />
              <h3>React</h3>
              <p>User interface</p>
            </article>
          </div>
        </section>

        <section className="about-section">
          <div className="about-section-heading">
            <span className="eyebrow">SYSTEM WORKFLOW</span>
            <h2>From image to assessment</h2>
          </div>

          <div className="about-workflow">
            <article className="about-workflow-step">
              <span>01</span>
              <i className="bi bi-camera" />
              <h3>Input</h3>
              <p>Capture or upload an image.</p>
            </article>
            <article className="about-workflow-step">
              <span>02</span>
              <i className="bi bi-bounding-box" />
              <h3>Detection</h3>
              <p>Locate jowar panicles with YOLO.</p>
            </article>
            <article className="about-workflow-step">
              <span>03</span>
              <i className="bi bi-diagram-3" />
              <h3>Classification</h3>
              <p>Estimate maturity with a separate classifier.</p>
            </article>
            <article className="about-workflow-step">
              <span>04</span>
              <i className="bi bi-clipboard-check" />
              <h3>Results</h3>
              <p>Display predictions for review.</p>
            </article>
          </div>
        </section>

        <div className="about-disclaimer">
          <i className="bi bi-info-circle" />
          <p>
            This is an academic prototype. Detection, maturity classification,
            and harvest-readiness assessment are separate tasks. Their
            performance must be evaluated before real-world use.
          </p>
        </div>
      </main>
      <Footer />
    </>
  );
}



function Detection() {
  const videoRef = useRef(null);
  const streamRef = useRef(null);
  const fileRef = useRef(null);

  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [apiResult, setApiResult] = useState(null);
  const [cameraOn, setCameraOn] = useState(false);
  const [imageUrl, setImageUrl] = useState('');
  const [fileName, setFileName] = useState('');
  const [message, setMessage] = useState('');
  const [capturedImage, setCapturedImage] = useState(null);

  // Stop camera and release image URL when leaving the page.
  useEffect(() => {
    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop());
      }

      if (imageUrl) {
        URL.revokeObjectURL(imageUrl);
      }
    };
  }, [imageUrl]);

  // Attach camera stream after rendering the video element.
  useEffect(() => {
    const video = videoRef.current;
    const stream = streamRef.current;

    if (cameraOn && video && stream) {
      video.srcObject = stream;

      video.play().catch(error => {
        console.error('Video playback error:', error);
        setMessage('Camera started, but the video preview could not play.');
      });
    }
  }, [cameraOn]);

  function stopCamera() {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }

    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }

    setCameraOn(false);
  }

  async function startCamera() {
    setMessage('');
    setApiResult(null);
    setCapturedImage(null);

    if (!navigator.mediaDevices?.getUserMedia) {
      setMessage('Camera is unavailable. Please upload an image instead.');
      return;
    }

    try {
      stopCamera();

      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'user' },
        audio: false
      });

      streamRef.current = stream;
      setCameraOn(true);
    } catch (error) {
      console.error('Camera error:', error);
      setCameraOn(false);

      if (error.name === 'NotAllowedError') {
        setMessage('Camera access was denied. Check your browser permissions.');
      } else if (error.name === 'NotReadableError') {
        setMessage('The camera may be busy. Close other apps using it and retry.');
      } else {
        setMessage(`Could not start camera: ${error.message}`);
      }
    }
  }

  function capturePhoto() {
    const video = videoRef.current;

    if (!video || !video.videoWidth || !video.videoHeight) {
      setMessage('Camera is not ready yet. Please wait and try again.');
      return;
    }

    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const context = canvas.getContext('2d');

    if (!context) {
      setMessage('Could not capture the photo. Please try again.');
      return;
    }

    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(blob => {
      if (!blob) {
        setMessage('Could not save the captured photo. Please try again.');
        return;
      }

      const photoFile = new File([blob], 'captured-jowar.jpg', {
        type: 'image/jpeg'
      });

      setCapturedImage(photoFile);

      setImageUrl(previousUrl => {
        if (previousUrl) URL.revokeObjectURL(previousUrl);
        return URL.createObjectURL(photoFile);
      });

      setFileName(photoFile.name);
      setApiResult(null);
      stopCamera();
      setMessage('Photo captured successfully. Click Analyze Image to detect panicles.');
    }, 'image/jpeg', 0.92);
  }

  function chooseImage(event) {
    const file = event.target.files?.[0];

    if (!file) return;

    if (!file.type.startsWith('image/')) {
      setMessage('Please select a valid image file.');
      event.target.value = '';
      return;
    }

    stopCamera();
    setCapturedImage(file);

    setImageUrl(previousUrl => {
      if (previousUrl) URL.revokeObjectURL(previousUrl);
      return URL.createObjectURL(file);
    });

    setFileName(file.name);
    setApiResult(null);
    setMessage('Image loaded successfully. Click Analyze Image to detect panicles.');

    // Allow selecting the same file again.
    event.target.value = '';
  }

  async function analyzeImage() {
    if (!capturedImage) {
      setMessage('Please capture a photo or upload an image first.');
      return;
    }

    setIsAnalyzing(true);
    setApiResult(null);
    setMessage('');

    try {
      const formData = new FormData();
      formData.append('file', capturedImage);

      const response = await fetch('http://127.0.0.1:8000/predict', {
        method: 'POST',
        body: formData
      });

      const data = await response.json();

      if (!response.ok) {
        const detail = data.detail;
        throw new Error(
          typeof detail === 'string'
            ? detail
            : detail?.message || 'The backend could not process the image.'
        );
      }

      setApiResult(data);
      setMessage('YOLO analysis completed successfully.');
    } catch (error) {
      console.error('API request failed:', error);
      setMessage(
        error.message || 'Could not connect to FastAPI. Check that the backend is running on port 8000.'
      );
    } finally {
      setIsAnalyzing(false);
    }
  }

  return (
    <>
      <Navbar />

      <main className="inner-page">
        <div className="page-title">
          <span className="eyebrow">IMAGE AND CAMERA INPUT</span>
          <h1>Panicle Detection</h1>
          <p>Use your camera or upload a jowar image to begin.</p>
        </div>

        <div className="detection-layout">
          <section className="content-card">
            <div className="card-heading">
              <h2>Image preview</h2>

              <span className={`status ${cameraOn ? 'status-live' : ''}`}>
                {cameraOn ? 'Camera active' : imageUrl ? 'Image ready' : 'Preview'}
              </span>
            </div>

            <div className="preview-area">
              {cameraOn ? (
                <video
                  ref={videoRef}
                  className="media-preview"
                  autoPlay
                  muted
                  playsInline
                />
              ) : imageUrl ? (
                <img
                  src={imageUrl}
                  className="media-preview"
                  alt="Selected jowar crop"
                />
              ) : (
                <div className="empty-preview">
                  <i className="bi bi-camera" />
                  <h3>No image selected</h3>
                  <p>Start the camera or upload a crop image.</p>
                </div>
              )}
            </div>

            <input
              ref={fileRef}
              type="file"
              accept="image/jpeg,image/png,image/webp"
              hidden
              onChange={chooseImage}
            />

            <div className="control-buttons">
              <button
                type="button"
                className="button button-primary"
                onClick={startCamera}
                disabled={cameraOn || isAnalyzing}
              >
                <i className="bi bi-camera-video" /> Start Camera
              </button>

              <button
                type="button"
                className="button button-secondary"
                onClick={stopCamera}
                disabled={!cameraOn}
              >
                Stop Camera
              </button>

              {cameraOn && (
                <button
                  type="button"
                  className="button button-secondary"
                  onClick={capturePhoto}
                >
                  <i className="bi bi-camera" /> Capture Photo
                </button>
              )}

              <button
                type="button"
                className="button button-secondary"
                onClick={() => fileRef.current?.click()}
                disabled={isAnalyzing}
              >
                <i className="bi bi-upload" /> Upload Image
              </button>

              <button
                type="button"
                className="button button-primary"
                onClick={analyzeImage}
                disabled={isAnalyzing || !capturedImage}
              >
                <i className="bi bi-cpu" />
                {isAnalyzing ? 'Analyzing...' : 'Analyze Image'}
              </button>
            </div>

            {fileName && (
              <p className="file-label">Selected: {fileName}</p>
            )}

            {message && (
              <p className="feedback-message" role="status">
                {message}
              </p>
            )}

            {apiResult && Array.isArray(apiResult.detections) && (
              <div className="detection-results">
                <span className="eyebrow">AI DETECTION OUTPUT</span>
                <h2>Analysis Results</h2>

                <div className="result-metrics">
                  <div>
                    <span>Panicles detected</span>
                    <strong>{apiResult.panicle_count}</strong>
                  </div>
                  <div>
                    <span>Detection model</span>
                    <strong>{apiResult.model}</strong>
                  </div>
                </div>

                {apiResult.detections.length === 0 ? (
                  <div className="info-box">
                    No panicles were detected in this image. Try another clear image.
                  </div>
                ) : (
                  apiResult.detections.map((detection, index) => (
                    <div className="info-box" key={index}>
                      <h3>Panicle {index + 1}</h3>

                      <p>
                        <strong>Class:</strong> {detection.class_name}
                      </p>

                      <p>
                        <strong>Confidence:</strong>{' '}
                        {(detection.confidence * 100).toFixed(2)}%
                      </p>

                      <p>
                        <strong>Bounding box (x1, y1, x2, y2):</strong>
                      </p>

                      <p>
                        {detection.bounding_box
                          .map(value => Number(value).toFixed(2))
                          .join(', ')}
                      </p>
                    </div>
                  ))
                )}
              </div>
            )}
          </section>

          <aside className="content-card details-card">
            <span className="eyebrow">ANALYSIS PIPELINE</span>
            <h2>How detection works</h2>

            <div className="pipeline-step">
              <span>1</span>
              <div>
                <strong>Input image</strong>
                <p>Capture a photo or upload an image.</p>
              </div>
            </div>

            <div className="pipeline-step">
              <span>2</span>
              <div>
                <strong>YOLO panicle detection</strong>
                <p>Locate panicles with bounding boxes and confidence scores.</p>
              </div>
            </div>

            <div className="pipeline-step">
              <span>3</span>
              <div>
                <strong>Maturity classification</strong>
                <p>A separate classifier is still required to estimate maturity.</p>
              </div>
            </div>

            <div className="info-box">
              <i className="bi bi-info-circle" />{' '}
              {apiResult
                ? 'YOLO inference completed. Review the detection results.'
                : capturedImage
                  ? 'Image is ready. Click Analyze Image to run YOLO detection.'
                  : 'Capture or upload an image to begin panicle detection.'}
            </div>

            <Link to="/results" className="button button-primary full-button">
              View Results Page <i className="bi bi-arrow-right" />
            </Link>
          </aside>
        </div>
      </main>

      <Footer />
    </>
  );
}


function Results() {
  return (
    <>
      <Navbar />
      <main className="inner-page">
        <div className="page-title">
          <span className="eyebrow">MODEL OUTPUT</span>
          <h1>Detection Results</h1>
          <p>Results will appear here when the model is connected.</p>
        </div>

        <section className="content-card results-placeholder">
          <div className="result-symbol"><i className="bi bi-bounding-box" /></div>
          <h2>Waiting for model output</h2>
          <p>
            After backend integration, this page can show the annotated image,
            panicle count, maturity stage, and model confidence.
          </p>

          <div className="result-metrics">
            <div><span>Panicles detected</span><strong>—</strong></div>
            <div><span>Maturity stage</span><strong>—</strong></div>
            <div><span>Confidence</span><strong>—</strong></div>
          </div>

          <Link to="/detect" className="button button-primary">
            Go to Detection <i className="bi bi-arrow-right" />
          </Link>
        </section>
      </main>
      <Footer />
    </>
  );
}

function History() {
  return (
    <>
      <Navbar />
      <main className="inner-page">
        <div className="page-title">
          <span className="eyebrow">PREVIOUS ANALYSES</span>
          <h1>Detection History</h1>
          <p>Review previous jowar analysis results.</p>
        </div>

        <section className="content-card empty-history">
          <i className="bi bi-clock-history" />
          <h2>No saved analyses yet</h2>
          <p>Saved results will appear here when history storage is implemented.</p>
          <Link to="/detect" className="button button-primary">
            Start Detection <i className="bi bi-arrow-right" />
          </Link>
        </section>
      </main>
      <Footer />
    </>
  );
}



function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  async function handleLogin(event) {
    event.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await fetch('http://127.0.0.1:8000/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          email: email.trim(),
          password
        })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          typeof data.detail === 'string'
            ? data.detail
            : 'Login failed. Please check your credentials.'
        );
      }

      // Save the returned token for subsequent authenticated requests.
      sessionStorage.setItem('jowarai_token', data.access_token);
      sessionStorage.setItem('jowarai_user', JSON.stringify(data.user));

      if (data.user.role === 'admin') {
        navigate('/admin');
      } else {
        navigate('/detect');
      }
    } catch (err) {
      setError(
        err.message || 'Unable to connect to the authentication server.'
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <Navbar />

      <main className="login-page">
        <section className="login-card">
          <div className="login-icon">
            <i className="bi bi-flower1" />
          </div>

          <span className="eyebrow">WELCOME TO JOWARAI</span>
          <h1>Sign in</h1>
          <p className="login-description">
            Sign in to access your JowarAI workspace.
          </p>

          <form onSubmit={handleLogin}>
            <label htmlFor="login-email">Email address</label>
            <input
              id="login-email"
              type="email"
              placeholder="you@example.com"
              value={email}
              onChange={event => setEmail(event.target.value)}
              autoComplete="username"
              required
            />

            <label htmlFor="login-password">Password</label>
            <div className="password-field">
              <input
                id="login-password"
                type={showPassword ? 'text' : 'password'}
                placeholder="Enter your password"
                value={password}
                onChange={event => setPassword(event.target.value)}
                autoComplete="current-password"
                required
              />

              <button
                type="button"
                className="password-toggle"
                onClick={() => setShowPassword(value => !value)}
                aria-label={showPassword ? 'Hide password' : 'Show password'}
              >
                <i className={`bi ${showPassword ? 'bi-eye-slash' : 'bi-eye'}`} />
              </button>
            </div>

            {error && (
              <p className="login-error" role="alert">
                {error}
              </p>
            )}

            <button
              type="submit"
              className="button button-primary login-submit"
              disabled={loading}
            >
              {loading ? 'Signing in...' : 'Sign In'}
              {!loading && <i className="bi bi-arrow-right" />}
            </button>
          </form>

          <Link to="/" className="login-home-link">
            <i className="bi bi-arrow-left" /> Back to Home
          </Link>
        </section>
      </main>

      <Footer />
    </>
  );
}
function Admin() {
  const stats = [
    { icon: 'bi-images', label: 'Images processed', value: '—' },
    { icon: 'bi-bounding-box', label: 'Panicles detected', value: '—' },
    { icon: 'bi-clock-history', label: 'Saved analyses', value: '0' },
    { icon: 'bi-cpu', label: 'AI model', value: 'YOLOv8' }
  ];

  return (
    <>
      <Navbar />
      <main className="inner-page admin-page">
        <div className="admin-heading">
          <div>
            <span className="eyebrow">PROJECT OVERVIEW</span>
            <h1>Admin Dashboard</h1>
            <p>Monitor the JowarAI prototype and access its main features.</p>
          </div>
          <span className="admin-badge">
            <i className="bi bi-shield-check" /> Admin Preview
          </span>
        </div>

        <div className="admin-notice">
          <i className="bi bi-info-circle" />
          This dashboard currently uses placeholder statistics. Live model
          metrics will appear after backend integration.
        </div>

        <section className="admin-stats">
          {stats.map(item => (
            <article className="admin-stat-card" key={item.label}>
              <div className="admin-stat-icon">
                <i className={`bi ${item.icon}`} />
              </div>
              <p>{item.label}</p>
              <h2>{item.value}</h2>
            </article>
          ))}
        </section>

        <section className="admin-content-grid">
          <article className="content-card admin-panel">
            <span className="eyebrow">SYSTEM STATUS</span>
            <h2>Project components</h2>

            <div className="admin-status-row">
              <span>Frontend interface</span>
              <span className="status status-live">Available</span>
            </div>
            <div className="admin-status-row">
              <span>YOLO panicle detection</span>
              <span className="status">Integration pending</span>
            </div>
            <div className="admin-status-row">
              <span>Maturity classifier</span>
              <span className="status">Integration pending</span>
            </div>
            <div className="admin-status-row">
              <span>Database and history</span>
              <span className="status">Not connected</span>
            </div>
          </article>

          <article className="content-card admin-panel">
            <span className="eyebrow">QUICK ACCESS</span>
            <h2>Project pages</h2>

            <Link to="/detect" className="admin-quick-link">
              <i className="bi bi-camera" />
              <span>Open Detection</span>
              <i className="bi bi-arrow-up-right" />
            </Link>
            <Link to="/results" className="admin-quick-link">
              <i className="bi bi-clipboard-data" />
              <span>View Results</span>
              <i className="bi bi-arrow-up-right" />
            </Link>
            <Link to="/history" className="admin-quick-link">
              <i className="bi bi-clock-history" />
              <span>Analysis History</span>
              <i className="bi bi-arrow-up-right" />
            </Link>
            <Link to="/about" className="admin-quick-link">
              <i className="bi bi-info-circle" />
              <span>About the Project</span>
              <i className="bi bi-arrow-up-right" />
            </Link>
          </article>
        </section>
      </main>
      <Footer />
    </>
  );
}


function ScrollToTop() {
  const { pathname } = useLocation();

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname]);

  return null;
}


function ProtectedRoute({ requiredRole }) {
  const token = sessionStorage.getItem('jowarai_token');
  const storedUser = sessionStorage.getItem('jowarai_user');

  let user = null;

  try {
    user = storedUser ? JSON.parse(storedUser) : null;
  } catch {
    user = null;
  }

  if (!token || !user || !user.role) {
    return <Navigate to="/login" replace />;
  }

  if (requiredRole && user.role !== requiredRole) {
    return <Navigate to="/detect" replace />;
  }

  return <Outlet />;
}


export default function App() {
  return (
    <BrowserRouter>
      <ScrollToTop />
      
<Routes>
  {/* Public pages */}
  <Route path="/" element={<Home />} />
  <Route path="/about" element={<About />} />
  <Route path="/login" element={<Login />} />

  {/* Pages available after login */}
  <Route element={<ProtectedRoute />}>
    <Route path="/detect" element={<Detection />} />
    <Route path="/analyze" element={<Detection />} />
    <Route path="/results" element={<Results />} />
    <Route path="/history" element={<History />} />
  </Route>

  {/* Admin-only page */}
  <Route element={<ProtectedRoute requiredRole="admin" />}>
    <Route path="/admin" element={<Admin />} />
  </Route>

  {/* Unknown URLs */}
  <Route path="*" element={<Navigate to="/" replace />} />
</Routes>

    </BrowserRouter>
  );
}
