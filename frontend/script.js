document.getElementById('styleForm').addEventListener('submit', async function(e) {
    e.preventDefault();
  
    const occasion = document.getElementById('occasion').value;
    const temperature = parseFloat(document.getElementById('temperature').value);
    const color_vibe = document.getElementById('color_vibe').value;
    const budget = document.getElementById('budget').value;
  
    const data = { occasion, temperature, color_vibe, budget, user_id: "demo_user" };
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '<div class="text-center text-light">Loading...</div>';
  
    try {
      const response = await fetch('http://127.0.0.1:8000/style', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
      });
  
      if (!response.ok) throw new Error('Backend error: ' + response.status);
  
      const result = await response.json();
      resultsDiv.innerHTML = '';
      result.outfits.forEach(outfit => {
        resultsDiv.innerHTML += `
          <div class="card">
            <h4>${outfit.name}</h4>
            <p>${outfit.description}</p>
            <span class="badge bg-secondary mb-2">${outfit.price}</span>
            <p class="text-success">${outfit.why || ''}</p>
            <button class="like-btn" onclick="sendFeedback('${outfit.name}', 'like')">👍 Like</button>
            <button class="dislike-btn" onclick="sendFeedback('${outfit.name}', 'dislike')">👎 Dislike</button>
          </div>
        `;
      });
      // Feedback text box
      resultsDiv.innerHTML += `
        <div class="card">
          <textarea id="commentBox" class="feedback-box" rows="2" placeholder="Tell us what you think..."></textarea>
          <button class="feedback-btn" onclick="sendComment()">Send Feedback</button>
        </div>
      `;
    } catch (err) {
      resultsDiv.innerHTML = `<div class="alert alert-danger">Error: ${err.message}</div>`;
    }
  });
  
  function sendFeedback(itemName, type) {
    let body = {user_id: "demo_user"};
    if (type === "like") body.liked_item_name = itemName;
    if (type === "dislike") body.disliked_item_name = itemName;
    fetch('http://127.0.0.1:8000/feedback', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(body)
    })
    .then(res => res.json())
    .then(data => {
      alert(type === "like" ? "Liked! Future suggestions will improve." : "Disliked! We'll avoid similar items.");
    });
  }
  
  function sendComment() {
    const comment = document.getElementById('commentBox').value;
    if (!comment) return;
    fetch('http://127.0.0.1:8000/comment', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({user_id: "demo_user", feedback: comment})
    })
    .then(res => res.json())
    .then(data => {
      alert("Thank you for your feedback!");
      document.getElementById('commentBox').value = "";
    });
  }
  
  function fillForm(type) {
    if (type === 'casual') {
      document.getElementById('occasion').value = 'casual';
      document.getElementById('temperature').value = 25;
      document.getElementById('color_vibe').value = 'neutrals';
      document.getElementById('budget').value = 'standard';
    } else if (type === 'office') {
      document.getElementById('occasion').value = 'office';
      document.getElementById('temperature').value = 22;
      document.getElementById('color_vibe').value = 'pastels';
      document.getElementById('budget').value = 'premium';
    } else if (type === 'evening') {
      document.getElementById('occasion').value = 'evening';
      document.getElementById('temperature').value = 20;
      document.getElementById('color_vibe').value = 'brights';
      document.getElementById('budget').value = 'premium';
    } else if (type === 'getaway') {
      document.getElementById('occasion').value = 'getaway';
      document.getElementById('temperature').value = 28;
      document.getElementById('color_vibe').value = 'neutrals';
      document.getElementById('budget').value = 'premium';
    } else if (type === 'random') {
      const occasions = ['casual', 'office', 'evening', 'getaway'];
      const vibes = ['neutrals', 'brights', 'pastels'];
      const budgets = ['standard', 'premium'];
      document.getElementById('occasion').value = occasions[Math.floor(Math.random()*occasions.length)];
      document.getElementById('temperature').value = Math.floor(Math.random()*16)+15;
      document.getElementById('color_vibe').value = vibes[Math.floor(Math.random()*vibes.length)];
      document.getElementById('budget').value = budgets[Math.floor(Math.random()*budgets.length)];
    }
  }
  