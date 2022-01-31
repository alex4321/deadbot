import io
import os
import time
import discord
import imagehash
from PIL import Image


CHECK_TYPES = {
    "image/bmp", "image/gif", "image/jpeg", "image/png"
}
TYPE2NAME = {
    "image/bmp": "image.bmp",
    "image/gif": "image.gif",
    "image/jpeg": "image.jpg",
    "image/png": "image.png",
}
REACTIONS = {
    '89cfa4f1e9a4590b': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    'c8b1b6bab1661d49': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    'a6a1f1d1e6ac1953': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    '8da3f2d4ada91a1a': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    'aca1f3d4acad131a': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    '99daa4f0eba45b0a': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    'aea0f1d1e4ac1b1b': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    '89d9a4b5f3aa114b': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    'a6a5f9d1a6ac1951': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    '89cda6f0eba4590b': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    '92e5ebe0e4ad1a43': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    '89b7f4e1a6a8154e': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    'c8b3b6b2b9600e5b': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    '89b3f4e3a4b81b4a': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    '89b3f4e1a4b85b4a': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    'a6a5f1d1a6ac1953': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    '9ba6ade1f2b70c10': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    'a6a4f1d3e4ac1b13': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    '8ca3f3d4ada91a1a': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    '89b7f4e2a2b8174c': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    'a6a0f1d3e6ac1b13': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    '9bdba4e4eba4130a': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    'aca0f1d3e4ac1b1b': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    '89b7f4e0a6b8174c': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    'c9b3a4f2b3e10e1a': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    'a6a0f1d1e6ac1b53': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    'a6a5f1d1a6ac1d51': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    '89dba4f1e9a4590b': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    'c8b1b6b8b9661d49': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    'c9b7a4f0f3a30c1a': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    '92e4e9e1e4b65b41': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    'aea0f1d3e4ac1b13': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    '96e5ebe0e4ad1a03': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    '89b3f4e1a6a4155e': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    '89d9a4f5eab4134a': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    'aca0f1d5e4ac1b1b': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    '9bd9a4f4eaa4134a': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    '9be6ade1f2a61910': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    '89cba6b0f3a61c4b': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    '9bdaa4e4eba41b0a': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    'aca1f3d6ccad1a0a': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    '8ca3f2d4eda91a1a': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    '89d9e4a5f16a194d': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    'aca0f3d4ecac131b': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    '94edeae0e5ad5203': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    '89cda4f1ebb4580b': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    '8cb3f6e0a6a6194b': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    'aca0f1d4ecac1b1b': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    'c9b3a4f0f3e30c1a': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    '92e4e9e1e4ae5b03': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    '8ca0f3d6cdad1a1a': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    'c9d3f6a1b356180b': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    'a6a5f9d0a6ac1d51': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    'c9b9f6f4a1661849': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    'ccb1b6b2b1661e49': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    'aca1f3d6c4ad1a1a': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    'aca3f3d4aca9131a': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    '8ca1f3d4eda91a1a': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    '89d9a4f5eab4194a': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    '89b7f4e2a6b8134c': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    'c9b3f4f1ab641849': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    '89dda4b5faa4114b': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    '8ca1f3d6ccad1a1a': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    '89d9a4b5f3ac114b': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    '89d9a4f5eaa4194b': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    '89b3f4a1a65c5b4a': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    'c9b3a6f1b364184b': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    '8ca1f3d4cdad1a1a': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    'aca1f3d4ccad1a1a': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    '9be4e9e1f6b61900': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    'ccb9f6f0a0a6194b': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    '89b3f6e0a6a41d4b': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    '89b3f4a5a35c1b0b': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    'd9b6acf0f2b30c12': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    '8993f4a5b35c1b0d': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    '8ca3f3d4aca91a5a': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    'aca0f1d3ecac1b13': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    '92e5ebe0e4ac5a43': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    '99dba4f0e9a4590b': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    'ccb1b6f0b1661e49': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    '99daa4f4eba41b0a': "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    "92e5ebe0e4ac5a43": "https://www.youtube.com/watch?v=xavhQ-uLOG0",
    "c9b3a6f1b364184b": "https://www.youtube.com/watch?v=xavhQ-uLOG0",
}
TIMEOUT = 60


class Robot(discord.Client):
    def __init__(self, reactions, *args, **kwargs):
        super(Robot, self).__init__(*args, **kwargs)
        self._last_message_send = None
        self._reactions = reactions

    def _to_image(self, content_type: str, content: bytes) -> list:
        store = io.BytesIO(content)
        store.seek(0)
        store.name = TYPE2NAME[content_type]
        if content_type != "image/gif":
            return [Image.open(store)]
        else:
            gif = Image.open(store)
            result = []
            for frame_index in range(gif.n_frames):
                gif.seek(frame_index)
                result.append(gif.convert("RGB"))
            return result

    def _can_send_message(self) -> bool:
        if self._last_message_send is None:
            return True
        return (time.time() - self._last_message_send) > TIMEOUT
    
    async def _send_message(self, channel, message):
        await channel.send(message)
        self._last_message_send = time.time()

    async def on_message(self, message: discord.Message):
        if len(message.attachments) == 0:
            return
        images = []
        for attachment in message.attachments:
            if attachment.content_type in CHECK_TYPES:
                content = await attachment.read()
                images += self._to_image(attachment.content_type, content)
        for image in images:
            hash = str(imagehash.phash(image))
            if hash in self._reactions and self._can_send_message():
                await self._send_message(message.channel, REACTIONS[hash])


if __name__ == "__main__":
    assert "DEADBOTTOKEN" in os.environ
    client = Robot(reactions=REACTIONS)
    client.run(os.environ.get("DEADBOTTOKEN"))
