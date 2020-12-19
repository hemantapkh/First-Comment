import click
from firstcomment import *

@click.command()
@click.option('--url','-u',prompt="Enter the URL", help='URL of the video')
@click.option('--method','-m',default='first-comment.com', help='Which method to use')


def hello(method, url):
    if method == 'first-comment.com':
        try:
            fc = firstComment(url)
        except InvalidUrl:
            print('[-] The URL you entered is not valid.');exit()

        except Exception:
            print('[-] Please check your internet connection.');exit()

        if fc.inDatabase:
            print(fc.luckMsg)
        else:
            print('Oh, this is the first time we hear about this video !\nWe are reading all of its comments to find the first commentor, wait for some time or come back later !')
            try:
                fc = firstComment(url, wait=True)
            except Exception:
                print('[-] Please check your internet connection.')
        
        print(f'\n{fc.title}\n')
        print(f'Comment: {fc.comment}')
        print(f'Author: {fc.author}')
        print(f'Autor URL: {fc.authorChannelUrl}')
        print(f'Published Date: {fc.publishedDate}')
        

hello()