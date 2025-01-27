from atproto import Client, client_utils, models
from .account_config import AccountConfig, MOAccountConfig, USAccountConfig
from .models.Bill import Bill
from .models.Enums import PartyCode, PoliticalParty
from .helpers import split_string_into_chunks
import math

def get_sponsor_counts(sponsors):
    party_counts = {
        PoliticalParty.REPUBLICAN.name: 0,
        PoliticalParty.DEMOCRAT.name: 0,
        PoliticalParty.INDEPENDENT.name: 0,
        PoliticalParty.LIBERTARIAN.name: 0,
        PoliticalParty.GREEN_PARTY.name: 0,
        PoliticalParty.NONPARTISAN.name: 0,
        'OTHER': 0
    }
    for sponsor in sponsors:
        party = sponsor.person.party
        if party in party_counts:
            party_counts[party] += 1
        else:
            party_counts['OTHER'] += 1
            
    party_counts_list = []
    
    for party, count in party_counts.items():
        if count > 0:
            party_counts_list.append((count, party))
    newline = '\n'
    party_counts_list.sort(reverse=True, key=lambda x: x[0])
    party_counts = f'{newline}- '.join([f'{party.title()}: {count}' for count, party in party_counts_list])
    
    sponsor_string = f'- {party_counts}'
    return sponsor_string

def create_detailed_post(bill: Bill, account_config: AccountConfig):
    text_builder = client_utils.TextBuilder()
    newline = '\n'
    sponsor_label = f'Sponsors:{newline}' if len(bill.sponsors) > 1 else 'Sponsor: '
    text_builder.tag(bill.bill_number, f'{account_config.code}{bill.bill_number}')
    text_builder.text(f": {bill.title}{newline}Status: {bill.last_action} {bill.last_action_date}{newline}{sponsor_label}")
    if len(bill.sponsors) == 1:
        party = PartyCode(int(bill.sponsors[0].person.party_id)).name
        text_builder.link(f"{bill.sponsors[0].person.name} ({party}) {bill.sponsors[0].person.district}",
                          f"https://ballotpedia.org/{bill.sponsors[0].person.ballotpedia}")
    else:
        if(isinstance(account_config, USAccountConfig)):
            sponsor_string = get_sponsor_counts(bill.sponsors)
            text_builder.link(sponsor_string,
                              bill.state_link+"?titles=hide&actionsOverview=hide&allActions=hide&committees=hide&relatedBills=hide&subjects=hide&latestSummary=hide")
            
        elif(isinstance(account_config, MOAccountConfig)):
            for sponsor in bill.sponsors:
                party = PartyCode(int(sponsor.person.party_id)).name
                text_builder.text("- ")
                text_builder.link(f"{sponsor.person.name} ({party}) {sponsor.person.district}",
                                  f"https://ballotpedia.org/{sponsor.person.ballotpedia}")
                text_builder.text(newline)
    return text_builder

def detailed_post_to_bsky(bill: Bill, client: Client, account_config: AccountConfig):
    state_link_embed = models.AppBskyEmbedExternal.Main(
        external = models.AppBskyEmbedExternal.External(
            title= f'More Info',
            description= f'{bill.bill_number}: {bill.title}',
            uri=bill.texts[0].state_link if len(bill.texts) > 0 else bill.state_link
        )
    )
    post = create_detailed_post(bill, account_config)
    if len(post.build_text()) <= 300:
        client.send_post(post, embed=state_link_embed)
        return
    else:
        multi_posts = create_multi_posts(post.build_text(), post.build_facets())
        for post in range(0, len(multi_posts)):
            if(post == 0):
                root = models.create_strong_ref(client.send_post(multi_posts[post][0], facets=multi_posts[post][1]))
                parent = models.create_strong_ref(root)
            else:
                if(post == len(multi_posts) - 1):
                    client.send_post(
                        multi_posts[post][0],
                        reply_to= models.AppBskyFeedPost.ReplyRef(parent=parent, root=root),
                        facets=multi_posts[post][1],
                        embed=state_link_embed
                    )
                else:
                    parent = models.create_strong_ref(client.send_post(
                        multi_posts[post][0],
                        reply_to= models.AppBskyFeedPost.ReplyRef(parent=parent, root=root),
                        facets=multi_posts[post][1]
                        ))
                    root = parent

def create_multi_posts(body, facets):
    chunks = split_string_into_chunks(body, 300)
    multi_posts = []
    chunk_indexes = [0]
    offset = 5.5
    for chunk in chunks:
        chunk_indexes.append(chunk_indexes[-1] + len(chunk))

    for i, chunk in enumerate(chunks):
        chunk_facets = []
        start_index = chunk_indexes[i]
        end_index = chunk_indexes[i + 1]

        for facet in facets:
            if start_index <= facet.index.byte_start < end_index:
                start = facet.index.byte_start - start_index + math.floor(offset * (i+1))
                end = min(
                        facet.index.byte_end - start_index + math.ceil(offset * (i+ 1)),
                        len(chunk)
                        )
                chunk_facets.append(
                    models.AppBskyRichtextFacet.Main(
                        index=models.AppBskyRichtextFacet.ByteSlice(byte_start=start, byte_end=end),
                        features=facet.features
                    )
                )

        multi_posts.append((chunk, chunk_facets))
    return multi_posts

def get_client(account_config):
    bsky_client = Client()
    bsky_client.login(
        account_config.bsky_user
        , account_config.bsky_password
        )
    return bsky_client