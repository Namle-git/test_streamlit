import streamlit as st

def render_permission_prompt():
    st.markdown("""
        <div id="permissionModal" style="display: none;">
            <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.5); display: flex; justify-content: center; align-items: center;">
                <div style="background-color: white; padding: 20px; border-radius: 5px;">
                    <h2>Requesting Microphone Access</h2>
                    <p>We need access to your microphone. Please allow access.</p>
                    <button id="grantPermissionButton">Allow</button>
                </div>
            </div>
        </div>
        <p id="status"></p>
        <script>
            document.getElementById('grantPermissionButton').addEventListener('click', function() {
                navigator.mediaDevices.getUserMedia({ audio: true })
                    .then(function(stream) {
                        document.getElementById('status').innerText = 'Microphone access granted';
                        document.getElementById('permissionModal').style.display = 'none';
                        console.log('Microphone access granted');
                    })
                    .catch(function(err) {
                        document.getElementById('status').innerText = 'Microphone access denied';
                        document.getElementById('permissionModal').style.display = 'none';
                        console.log('Microphone access denied', err);
                    });
            });

            function showModal() {
                document.getElementById('permissionModal').style.display = 'block';
            }

            function hideModal() {
                document.getElementById('permissionModal').style.display = 'none';
            }

            showModal();
        </script>
    """, unsafe_allow_html=True)

# Streamlit app
st.title("Microphone Access Request")

# Render the permission prompt modal
render_permission_prompt()

# Add some description
st.write("This app requires access to your microphone. Please grant permission to continue.")
